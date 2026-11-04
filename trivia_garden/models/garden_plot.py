from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GardenPlot(models.Model):
    _name = "garden.plot"
    _description = "Garden Plot"
    _order = "site_id, name"

    name = fields.Char(required=True)
    site_id = fields.Many2one("garden.site", string="Site", required=True, ondelete="cascade")
    area = fields.Float(string="Area (m²)")
    tenant_id = fields.Many2one("res.partner", string="Tenant", index=True)

    # ----------------------------------------------------------------------------
    # TODO 6 - The rules of the plots
    #
    # A plot can only be rented (tenant_id) by a member who paid the fee of the
    # current year (see last_paid_year, TODO 4), and a member rents one plot at most.
    # Refuse the other cases with a clear message.
    # ----------------------------------------------------------------------------

    @api.constrains('site_id', 'tenant_id')
    def _check_tenant_status(self):
        self.flush_model(['tenant_id', 'site_id'])
        current_year = fields.Datetime.today().year
        for record in self.filtered('tenant_id'):
            tenant = record.tenant_id
            if not tenant.last_paid_year >= current_year:
                raise ValidationError("Teannt %s can not rent a plot as it didn't pay his membership fees this year" % (
                    tenant.display_name,
                ))
            other_site = self.search([('tenant_id', '=', tenant.id), ('id', '!=', record.id)])
            if other_site:
                raise ValidationError("Tenant %s is already renting plot %s" % (
                    tenant.display_name, other_site.display_name,
                ))
