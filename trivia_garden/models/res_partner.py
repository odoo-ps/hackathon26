from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # ----------------------------------------------------------------------------
    # TODO 4 - The members
    #
    # Add the fields of the members to the contacts:
    #   * membership_type   Selection individual / family / patron      "Membership Type"
    #   * member_since      Date                                         "Member Since"
    #   * fee_ids           One2many to garden.membership.fee            "Membership Fees"
    #   * last_paid_year    Integer, computed and STORED                 "Last Paid Year"
    #                       the most recent year of a PAID fee, 0 if none
    #
    # last_paid_year must always be up to date: when a fee is paid, when its year
    # changes, when a fee is added or deleted.
    # ----------------------------------------------------------------------------

    membership_type = fields.Selection([
        ("individual", "Individual"),
        ("family", "Family"),
        ("patron", "Patron"),
    ], default="individual")
    member_since = fields.Date()
    fee_ids = fields.One2many("garden.membership.fee", "partner_id", string="Membership Fees")
    last_paid_year = fields.Integer(
        compute="_compute_last_paid_year", store=True,
    )

    @api.depends('fee_ids.state', 'fee_ids.year')
    def _compute_last_paid_year(self):
        partners_last_paid = dict(self.env["garden.membership.fee"]._read_group(
            [('partner_id', 'in', self.ids), ('state', '=', 'paid')],
            groupby=['partner_id'],
            aggregates=['year:max'],
        ))
        for record in self:
            record.last_paid_year = partners_last_paid.get(record, 0)

    def action_open_membership_fees(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('trivia_garden.garden_membership_fee_action')
        action['domain'] = [('partner_id', '=', self.id)]
        return action
