from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProductionPlan(models.Model):
    _name = "bz.production.plan"
    _description = "Production Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start desc, id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    date_end = fields.Date(string="End Date", required=True, tracking=True)
    user_id = fields.Many2one(
        "res.users",
        string="Responsible",
        default=lambda self: self.env.user,
        tracking=True,
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        required=True,
        copy=False,
        tracking=True,
    )
    line_ids = fields.One2many(
        "bz.production.plan.line", "plan_id", string="Plan Lines", copy=True
    )
    production_ids = fields.One2many(
        "mrp.production", "bz_plan_id", string="Manufacturing Orders"
    )
    production_count = fields.Integer(compute="_compute_production_count")
    total_qty = fields.Float(
        string="Total Quantity",
        compute="_compute_total_qty",
        digits="Product Unit of Measure",
    )
    progress = fields.Float(
        string="Progress (%)",
        compute="_compute_progress",
        help="Share of manufacturing orders from this plan that are done.",
    )
    note = fields.Html()

    @api.depends("production_ids")
    def _compute_production_count(self):
        for plan in self:
            plan.production_count = len(plan.production_ids)

    @api.depends("line_ids.product_qty")
    def _compute_total_qty(self):
        for plan in self:
            plan.total_qty = sum(plan.line_ids.mapped("product_qty"))

    @api.depends("production_ids.state")
    def _compute_progress(self):
        for plan in self:
            productions = plan.production_ids.filtered(lambda p: p.state != "cancel")
            done = productions.filtered(lambda p: p.state == "done")
            plan.progress = 100.0 * len(done) / len(productions) if productions else 0.0

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        for plan in self:
            if plan.date_end and plan.date_start and plan.date_end < plan.date_start:
                raise ValidationError(_("The end date must be on or after the start date."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("bz.production.plan") or _("New")
        return super().create(vals_list)

    def unlink(self):
        if any(plan.state not in ("draft", "cancel") for plan in self):
            raise UserError(_("You can only delete draft or cancelled plans."))
        return super().unlink()

    def action_confirm(self):
        for plan in self:
            if not plan.line_ids:
                raise UserError(_("Add at least one product before confirming the plan."))
        self.write({"state": "confirmed"})

    def action_generate_productions(self):
        """Create one manufacturing order per plan line that does not have one yet."""
        Production = self.env["mrp.production"]
        for plan in self:
            if plan.state != "confirmed":
                raise UserError(_("Confirm the plan before generating manufacturing orders."))
            for line in plan.line_ids.filtered(lambda l: not l.production_id):
                bom = line.bom_id or line._find_bom()
                if not bom:
                    raise UserError(
                        _("No bill of materials found for %(product)s.", product=line.product_id.display_name)
                    )
                line.production_id = Production.create(
                    {
                        "product_id": line.product_id.id,
                        "product_qty": line.product_qty,
                        "product_uom_id": line.product_uom_id.id,
                        "bom_id": bom.id,
                        "date_start": fields.Datetime.to_datetime(line.date_planned),
                        "origin": plan.name,
                        "company_id": plan.company_id.id,
                        "bz_plan_id": plan.id,
                    }
                )
        return self.action_view_productions()

    def action_done(self):
        for plan in self:
            pending = plan.production_ids.filtered(lambda p: p.state not in ("done", "cancel"))
            if pending:
                raise UserError(
                    _("These manufacturing orders are not finished yet: %(orders)s",
                      orders=", ".join(pending.mapped("name")))
                )
        self.write({"state": "done"})

    def action_cancel(self):
        for plan in self:
            started = plan.production_ids.filtered(lambda p: p.state not in ("draft", "cancel"))
            if started:
                raise UserError(
                    _("Cancel or finish these manufacturing orders first: %(orders)s",
                      orders=", ".join(started.mapped("name")))
                )
            plan.production_ids.filtered(lambda p: p.state == "draft").action_cancel()
        self.write({"state": "cancel"})

    def action_draft(self):
        self.filtered(lambda p: p.state == "cancel").write({"state": "draft"})

    def action_view_productions(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("mrp.mrp_production_action")
        action["domain"] = [("bz_plan_id", "=", self.id)]
        action["context"] = {"default_bz_plan_id": self.id, "create": False}
        if self.production_count == 1:
            action["view_mode"] = "form"
            action["views"] = [(False, "form")]
            action["res_id"] = self.production_ids.id
        return action
