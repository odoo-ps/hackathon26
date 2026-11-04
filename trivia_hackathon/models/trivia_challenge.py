import hashlib
import hmac
import logging
from contextlib import closing
from typing import NamedTuple

from lxml import etree
from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import remove_accents
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import html_translate

_logger = logging.getLogger(__name__)

WEDGE_COLORS = [
    ("blue", "Blue"),
    ("green", "Green"),
    ("yellow", "Yellow"),
    ("pink", "Pink"),
    ("orange", "Orange"),
    ("purple", "Purple"),
]
WEDGES = {
    "blue": "🔵",
    "green": "🟢",
    "yellow": "🟡",
    "pink": "🩷",
    "orange": "🟠",
    "purple": "🟣",
}
EMPTY_WEDGE = "⚪"

# The flag revealed by a checker only depends on the code of the challenge: on Odoo.sh, each push
# rebuilds the database, and the teams submit their flags again to get their wedges back.
FLAG_SECRET = b"trivia-hackathon-2026"


class CheckFailed(Exception):
    """ Raised by a checker step when a requirement of the challenge is not met. """


class CheckResult(NamedTuple):
    label: str
    passed: bool
    detail: str = ""
    bonus: bool = False


def require(condition, message):
    """ Make the current checker step fail with ``message`` unless ``condition`` holds. """
    if not condition:
        raise CheckFailed(message)


def normalize(text):
    """ Return ``text`` without accents nor case: "Mécénat" and "mecenat" are the same. """
    return remove_accents(text or "").strip().lower()


def name_matches(typed, expected):
    """ Whether a name typed by the players matches the ``expected`` one, leniently: without accents nor case,
    in the singular or the plural, with more words or longer words. Each word of ``expected`` must start a word
    of ``typed``: "Meuble" and "Meubles", "Électroménager" and "Électro", "Atelier de réparation" and
    "Atelier réparation" match. """
    words = normalize(typed).split()
    return all(any(word.startswith(part.rstrip("s")) for word in words) for part in normalize(expected).split())


def get_arch(model, view_type, view_id=None):
    """ Return the arch (lxml) of a view of ``model``, with all its inherited views applied. """
    return etree.fromstring(model.get_view(view_id=view_id, view_type=view_type)["arch"])


def eval_expression(expression, values):
    """ Evaluate a view expression (invisible, readonly, decoration-*...) with the given values.

    :return: True or False, or None when it can't be evaluated (e.g. it uses other fields)
    """
    try:
        return bool(safe_eval(expression, values))
    except Exception:  # noqa: BLE001
        return None


class TriviaChallenge(models.Model):
    """ A challenge of the game board, brought by the module of a non-profit organisation.

    A challenge is validated by the method ``_check_<code>()`` that its module adds to this model.
    It returns a list of results, one per step, made by ``_run_step()``.
    """
    _name = "trivia.challenge"
    _description = "Trivia Challenge"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, readonly=True, help="Technical identifier, the checker method is _check_<code>.")
    organization = fields.Char(string="Organisation", help="The non-profit organisation that needs your help.")
    topic = fields.Char(translate=True)
    summary = fields.Text(string="Instruction", translate=True, help="Short instruction displayed on the game board.")
    description = fields.Html(string="Statement", translate=html_translate)
    difficulty = fields.Selection(
        [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
        required=True, default="easy",
    )
    wedge_color = fields.Selection(WEDGE_COLORS, required=True, default="blue")
    wedge = fields.Char(compute="_compute_wedge")
    state = fields.Selection([("todo", "To do"), ("solved", "Solved")], required=True, default="todo", readonly=True)
    solved_date = fields.Datetime(readonly=True)
    solved_by_id = fields.Many2one("res.users", string="Solved By", readonly=True)
    attempt_count = fields.Integer(string="Attempts", readonly=True)
    flag = fields.Char(readonly=True, help="Keep it: submit it again to get the wedge back on a new database.")
    checker_report = fields.Html(readonly=True)
    star_count = fields.Integer(string="Bonus Objectives Reached", readonly=True)
    star_total = fields.Integer(string="Bonus Objectives", readonly=True)
    stars = fields.Char(string="Bonus", compute="_compute_stars")
    board = fields.Char(compute="_compute_board")

    _code_uniq = models.Constraint("UNIQUE(code)", "The code of a challenge must be unique.")

    @api.depends("wedge_color", "state")
    def _compute_wedge(self):
        for challenge in self:
            challenge.wedge = WEDGES[challenge.wedge_color] if challenge.state == "solved" else EMPTY_WEDGE

    @api.depends("star_count", "star_total")
    def _compute_stars(self):
        for challenge in self:
            challenge.stars = "⭐" * challenge.star_count + "☆" * (challenge.star_total - challenge.star_count)

    def _compute_board(self):
        board = self._get_board()
        for challenge in self:
            challenge.board = board

    @api.model
    def _get_board(self):
        return " ".join(self.sudo().search([]).mapped("wedge"))

    # ------------------------------------------------------------------
    # Game engine
    # ------------------------------------------------------------------

    def action_open_flag_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Submit a flag"),
            "res_model": "trivia.flag.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_challenge_id": self.id},
        }

    def action_run_checker(self):
        self.ensure_one()
        checker = getattr(self, f"_check_{self.code}", None)
        if not checker:
            raise UserError(self.env._("This challenge has no automatic checker."))
        results = checker()
        failed = [result for result in results if not result.passed and not result.bonus]
        bonus = [result for result in results if result.bonus]
        challenge = self.sudo()
        vals = {
            "attempt_count": challenge.attempt_count + 1,
            "checker_report": self._render_checker_report(results),
            "star_count": len([result for result in bonus if result.passed]),
            "star_total": len(bonus),
        }
        if not failed:
            vals["flag"] = challenge._get_checker_flag()
        challenge.write(vals)
        if self.env.context.get("trivia_open_challenge"):
            # checked from the game board: show the report
            next_action = {
                "type": "ir.actions.act_window",
                "res_model": self._name,
                "res_id": self.id,
                "views": [(False, "form")],
            }
        else:
            next_action = {"type": "ir.actions.client", "tag": "soft_reload"}
        if failed:
            message = self.env._("%(failed)s requirement(s) not met yet, see the checker report.", failed=len(failed))
            return self._notify(message, "warning", next_action)
        if challenge.state != "solved":
            challenge._mark_solved()
        message = self.env._("All requirements are met, you won the %(wedge)s wedge!", wedge=WEDGES[self.wedge_color])
        return self._notify(message, "success", next_action)

    def _submit_flag(self, flag):
        """ Return whether ``flag`` is the flag of this challenge, mark it as solved if so. """
        self.ensure_one()
        challenge = self.sudo()
        challenge.attempt_count += 1
        flag = (flag or "").strip()
        if not hmac.compare_digest(flag.encode(), challenge._get_checker_flag().encode()):
            return False
        if challenge.state != "solved":
            challenge.flag = flag
            challenge._mark_solved()
        return True

    def _get_checker_flag(self):
        self.ensure_one()
        digest = hmac.new(FLAG_SECRET, self.code.encode(), hashlib.sha256).hexdigest()[:12]
        return f"TRIVIA{{{self.code}_{digest}}}"

    def _mark_solved(self):
        for challenge in self:
            challenge.write({
                "state": "solved",
                "solved_date": fields.Datetime.now(),
                "solved_by_id": self.env.uid,
            })
            challenge._announce_wedge()

    def _announce_wedge(self):
        """ Post the won wedge and the current board in the Trivi'Hackathon channel. """
        self.ensure_one()
        channel = self.env.ref("trivia_hackathon.channel_trivia", raise_if_not_found=False)
        if not channel:
            return
        message = self.env._(
            "%(user)s won the %(wedge)s wedge of “%(challenge)s” (%(organization)s)!",
            user=self.env.user.name, wedge=WEDGES[self.wedge_color],
            challenge=self.name, organization=self.organization,
        )
        body = Markup('<p>%s</p><p style="font-size: 2rem;">%s</p>') % (message, self._get_board())
        if all(state == "solved" for state in self.sudo().search([]).mapped("state")):
            body += Markup("<p><b>%s</b></p>") % self.env._("🧀 The cheese is complete, congratulations!")
        channel.sudo().message_post(
            body=body,
            author_id=self.env.ref("base.partner_root").id,
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
        )

    def _notify(self, message, notification_type, next_action=None):
        params = {"message": message, "type": notification_type, "sticky": False}
        if next_action:
            params["next"] = next_action
        return {"type": "ir.actions.client", "tag": "display_notification", "params": params}

    # ------------------------------------------------------------------
    # Tools for the checkers
    # ------------------------------------------------------------------

    def _run_step(self, label, step, bonus=False):
        """ Run a checker step in a savepoint which is always rolled back, so that the records
        created to check the challenge never stay in the database.

        :param str label: what the step checks, displayed in the report
        :param step: function without argument, raising ``CheckFailed`` (see ``require()``)
            when a requirement is not met
        :param bool bonus: whether the step is a bonus objective, which is not needed to win the wedge
        :rtype: CheckResult
        """
        try:
            # closing(): the savepoint is rolled back on exit, whether the step passes or fails
            with closing(self.env.cr.savepoint()):
                step()
        except CheckFailed as e:
            return CheckResult(label, False, str(e), bonus)
        except Exception as e:  # noqa: BLE001 - the code of the challengers may raise anything
            _logger.info("Trivi'Hackathon checker step %r crashed", label, exc_info=True)
            detail = self.env._("Your code raised %(error)s", error=f"{type(e).__name__}: {e}")
            return CheckResult(label, False, detail, bonus)
        return CheckResult(label, True, bonus=bonus)

    @api.model
    def _render_checker_report(self, results):
        def icon(result):
            if result.bonus:
                return "⭐" if result.passed else "☆"
            return "✅" if result.passed else "❌"

        items = Markup().join(
            Markup('<li class="mb-2">%s <b>%s</b>%s</li>') % (
                icon(result),
                self.env._("Bonus: %(label)s", label=result.label) if result.bonus else result.label,
                Markup("<br/><i>%s</i>") % result.detail if result.detail else "",
            )
            for result in results
        )
        return Markup('<ul class="list-unstyled">%s</ul>') % items
