from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bz_line_note = fields.Char(
        string="Line Note",
        help="Short note for this product, printed on the sales summary.",
    )
