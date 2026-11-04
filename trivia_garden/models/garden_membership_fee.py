# ----------------------------------------------------------------------------
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
import datetime

from odoo import fields, models


class GardenMembershipFee(models.Model):
    _name = 'garden.membership.fee'
    _description = "Garden Membership Fee"

    partner_id = fields.Many2one('res.partner', string='Member', required=True)
    year = fields.Integer(default=datetime.datetime.now().year, required=True)
    amount = fields.Float()
    state = fields.Selection(string='Status',
                             selection=[('draft', 'Draft'),('paid', 'Paid')],
                             default='draft',
                             required=True)
    payment_date = fields.Date()

    # Not exactly correct but will do for now
    _check_max_one_payment = models.Constraint(
        'UNIQUE(partner_id, year, state)',
        'A user should not pay more than one fee per year.',
    )
    def action_mark_paid(self):
        return self.write({'state': 'paid', 'payment_date': str(datetime.date.today())})
