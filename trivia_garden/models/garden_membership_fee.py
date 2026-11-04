# ----------------------------------------------------------------------------
# TODO 1 - The membership fees
#
# Create the model garden.membership.fee ("Membership Fee"), with the fields:
#   * partner_id     Many2one to res.partner, required     "Member"
#   * year           Integer, required                      "Year"
#   * amount         Float (or Monetary)                    "Amount"
#   * state          Selection draft / paid, required,      "Status"
#                    "draft" by default
#   * payment_date   Date                                   "Payment Date"
#
# A member pays at most one fee per year: add a constraint.
# Add the method action_mark_paid(), which marks the fees as paid today.
# ----------------------------------------------------------------------------

from odoo import models, fields


class GardenMembershipFee(models.Model):
    _name = "garden.membership.fee"

    partner_id = fields.Many2one("res.partner", string="Member", required=True)
    year = fields.Integer(string="Year", copy=False, required=True)
    amount = fields.Float(string="Amount")
    state = fields.Selection([("draft", "Draft"), ("paid", "Paid")], default='draft', string="State", required=True, copy=False)
    payment_date = fields.Date("Payment Date", readonly=True, copy=False)

    _name_uniq = models.Constraint(
        'unique(partner_id, year)',
        'Member can pay at most once a year.',
    )

    def action_mark_paid(self):
        self.write({
            'state': 'paid',
            'payment_date': fields.Date.today(),
        })
