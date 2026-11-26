from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductionPlanLine(models.Model):
    _name = "bz.production.plan.line"
    _description = "Production Plan Line"
    _order = "date_planned, id"

    plan_id = fields.Many2one(
        "bz.production.plan", required=True, ondelete="cascade", index=True
    )
    company_id = fields.Many2one(related="plan_id.company_id", store=True)
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain="[('type', '=', 'consu')]",
    )
    product_tmpl_id = fields.Many2one(related="product_id.product_tmpl_id")
    bom_id = fields.Many2one(
        "mrp.bom",
        string="Bill of Materials",
        domain="[('product_tmpl_id', '=', product_tmpl_id), '|', ('product_id', '=', False), ('product_id', '=', product_id)]",
    )
    product_qty = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
        digits="Product Unit of Measure",
    )
    product_uom_id = fields.Many2one(related="product_id.uom_id", string="Unit")
    date_planned = fields.Date(string="Planned Date", required=True)
    production_id = fields.Many2one(
        "mrp.production", string="Manufacturing Order", readonly=True, copy=False
    )
    production_state = fields.Selection(
        related="production_id.state", string="MO Status"
    )

    _sql_constraints = [
        ("qty_positive", "CHECK(product_qty > 0)", "The quantity must be greater than zero."),
    ]

    @api.constrains("date_planned", "plan_id")
    def _check_date_in_plan(self):
        for line in self:
            plan = line.plan_id
            if line.date_planned and not plan.date_start <= line.date_planned <= plan.date_end:
                raise ValidationError(
                    _("The planned date of %(product)s must be between the plan start and end dates.",
                      product=line.product_id.display_name)
                )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        self.bom_id = self._find_bom() if self.product_id else False
        if not self.date_planned and self.plan_id:
            self.date_planned = self.plan_id.date_start

    def _find_bom(self):
        self.ensure_one()
        boms = self.env["mrp.bom"]._bom_find(
            self.product_id,
            company_id=self.plan_id.company_id.id or self.env.company.id,
            bom_type="normal",
        )
        return boms[self.product_id]
