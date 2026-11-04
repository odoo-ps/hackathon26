from odoo import fields, models, tools
from odoo.tools import SQL

from ..models.run_runner import CATEGORIES, GENDERS


class RunResultReport(models.Model):
    """ The results of the races: one row per runner who reached the finish. """
    _name = "run.result.report"
    _description = "Race Results"
    _auto = False  # no table: the model reads the SQL view created by init()
    _order = "edition_id desc, rank, bib"

    runner_id = fields.Many2one("run.runner", string="Runner", readonly=True)
    edition_id = fields.Many2one("run.edition", string="Edition", readonly=True)
    bib = fields.Integer(readonly=True)
    category = fields.Selection(CATEGORIES, readonly=True)
    gender = fields.Selection(GENDERS, readonly=True)
    finish_time = fields.Float(string="Time (min)", readonly=True, aggregator="avg")
    pace = fields.Float(string="Pace (min/km)", readonly=True, aggregator="avg")
    rank = fields.Integer(readonly=True, aggregator="min")
    category_rank = fields.Integer(string="Rank in Category", readonly=True, aggregator="min")

    def init(self):
        """ Create the SQL view of the results (called when the module is installed or updated).

        TODO 1 - Replace this empty placeholder by the real results: one row per runner who
        reached the finish (a split at km 10), with the columns:

        * id: the id of the runner (each row of a model needs a unique id)
        * runner_id, edition_id, bib, category, gender: from the runner
        * finish_time: the minutes between the start (split at km 0) and the finish (split at km 10)
        * pace: the minutes per km (the race is 10 km long)
        * rank: the rank in the edition, the fastest first; runners with the same time share
          the same rank (1, 2, 2, 4)
        * category_rank: the same, within the category of the runner

        Tips: EXTRACT(EPOCH FROM <interval>) gives seconds, and the window functions
        RANK() OVER (PARTITION BY ... ORDER BY ...) compute ranks.
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(SQL(
            """
            CREATE OR REPLACE VIEW %s AS (
                 SELECT runner.id,
                        runner.id AS runner_id,
                        runner.edition_id,
                        runner.bib,
                        runner.category,
                        runner.gender,
                        started.time AS start_time,
                        ended.time AS end_time,
                        EXTRACT(EPOCH FROM (ended.time - started.time)) / 60.0 AS finish_time,
                        EXTRACT(EPOCH FROM (ended.time - started.time)) / 60.0 / 10.0 AS pace,
                        RANK() OVER (PARTITION BY edition_id ORDER BY (ended.time - started.time) ASC) AS rank,
                        RANK() OVER (PARTITION BY edition_id, category ORDER BY (ended.time - started.time) ASC) AS category_rank

                   FROM run_split AS started
                   JOIN run_runner AS runner ON (started.runner_id = runner.id)
                   JOIN run_split AS ended ON (ended.runner_id = started.runner_id AND ended.checkpoint_km = 10)
                  WHERE started.checkpoint_km = 0  -- attented and started the run
                    AND runner.disqualified IS NOT true
            )
            """,
            SQL.identifier(self._table),
        ))
