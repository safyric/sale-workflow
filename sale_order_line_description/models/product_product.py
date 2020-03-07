# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

        
    sale_order_line_id = fields.Many2one('sale.order.line', string='Sale order line')
