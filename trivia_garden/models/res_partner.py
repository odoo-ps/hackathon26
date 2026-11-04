from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    membership_type = fields.Selection(
        [("individual", "Individual"), ("family", "Family"), ("patron", "Patron")], string="Membership Type",
    )
    member_since = fields.Date()
    fee_ids = fields.One2many("garden.membership.fee", "partner_id", string="Membership Fees")
    last_paid_year = fields.Integer(compute="_compute_last_paid_year", store=True)

    @api.depends("fee_ids.state", "fee_ids.year")
    def _compute_last_paid_year(self):
        for partner in self:
            paid_years = partner.fee_ids.filtered(lambda fee: fee.state == "paid").mapped("year")
            partner.last_paid_year = max(paid_years, default=0)
