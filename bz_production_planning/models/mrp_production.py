from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    bz_plan_id = fields.Many2one(
        "bz.production.plan",
        string="Production Plan",
        readonly=True,
        copy=False,
        index=True,
    )
