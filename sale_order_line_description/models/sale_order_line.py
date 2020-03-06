# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _get_sale_order_line_multiline_description_sale(self, product):
        res = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_sale(product)
        return self._get_sale_order_line_multiline_description_variants()

        return res
    
    def _get_sale_order_line_multiline_description_variants(self):
        res1 = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_variants()
        product_attribute_with_is_custom = self.product_custom_attribute_value_ids.mapped('attribute_value_id.attribute_id')
        
        # display the no_variant attributes, except those that are also
        # displayed by a custom (avoid duplicate)
        for no_variant_attribute_value in self.product_no_variant_attribute_value_ids.filtered(
            lambda ptav: ptav.attribute_id not in product_attribute_with_is_custom
        ):
            name += "\n" + no_variant_attribute_value.attribute_id.name + ': ' + no_variant_attribute_value.name
            
        # display the is_custom values
        for pacv in self.product_custom_attribute_value_ids:
            name += "\n" + pacv.attribute_value_id.attribute_id.name + \
            ': ' + (pacv.custom_value or '').strip()
        return name        
        
        return res1
