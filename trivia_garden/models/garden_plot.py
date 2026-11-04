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

    _tenant_uniq = models.Constraint("UNIQUE(tenant_id)", "A member rents one plot at most.")

    @api.constrains("tenant_id")
    def _check_tenant_paid(self):
        this_year = fields.Date.context_today(self).year
        for plot in self:
            if plot.tenant_id and plot.tenant_id.last_paid_year < this_year:
                raise ValidationError(self.env._(
                    "%(member)s did not pay the fee of %(year)s: they cannot rent a plot.",
                    member=plot.tenant_id.name, year=this_year,
                ))
