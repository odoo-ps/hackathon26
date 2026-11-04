from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    # ----------------------------------------------------------------------------
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
        ('individual', 'Individual'),
        ('family', 'Family'),
        ('patron', 'Patron')
    ], default='individual')
    member_since = fields.Datetime()
    fee_ids = fields.One2many('garden.membership.fee', 'partner_id', string='Membership Fees')
    last_paid_year = fields.Integer(compute='_compute_last_paid_year', store=True)

    @api.depends('fee_ids.state','fee_ids.year')
    def _compute_last_paid_year(self):
        for record in self:
            paid_fees = record.fee_ids.filtered(lambda fee: fee.partner_id.id == record.id and fee.state == 'paid')
            if paid_fees:
                record.last_paid_year = max(paid_fees.mapped('year'))
            else:
                record.last_paid_year = 0
