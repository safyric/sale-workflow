from odoo import api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale order line')
