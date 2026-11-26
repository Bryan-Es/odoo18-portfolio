from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bz_delivery_deadline = fields.Date(
        string="Delivery Deadline",
        tracking=True,
        help="Date the customer needs the goods. Printed on the sales summary.",
    )
    bz_sale_channel = fields.Selection(
        [
            ("store", "Store"),
            ("phone", "Phone"),
            ("whatsapp", "WhatsApp"),
            ("web", "Website"),
            ("other", "Other"),
        ],
        string="Sales Channel",
        default="store",
        tracking=True,
    )
    bz_internal_note = fields.Text(
        string="Internal Note",
        help="Visible to your team only. Not printed for the customer.",
    )
    bz_days_to_deadline = fields.Integer(
        string="Days Left",
        compute="_compute_bz_days_to_deadline",
        help="Days until the delivery deadline. Negative means it is late.",
    )
    bz_total_qty = fields.Float(
        string="Total Quantity",
        compute="_compute_bz_total_qty",
        digits="Product Unit of Measure",
    )

    @api.depends("bz_delivery_deadline")
    def _compute_bz_days_to_deadline(self):
        today = fields.Date.context_today(self)
        for order in self:
            order.bz_days_to_deadline = (
                (order.bz_delivery_deadline - today).days if order.bz_delivery_deadline else 0
            )

    @api.depends("order_line.product_uom_qty", "order_line.display_type")
    def _compute_bz_total_qty(self):
        for order in self:
            lines = order.order_line.filtered(lambda l: not l.display_type)
            order.bz_total_qty = sum(lines.mapped("product_uom_qty"))
