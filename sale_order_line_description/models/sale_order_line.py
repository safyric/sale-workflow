# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    @api.multi
    def get_sale_order_line_multiline_description_sale(self, product):
        res = super(SaleOrderLine,self).get_sale_order_line_multiline_description_sale(product)
        if product.description_sale:
            return '[' + product.default_code + ']' \
                + "\n" + self._get_sale_order_line_multiline_description_variants() \
                + product.description_sale
        return '[' + product.default_code + ']' \
            + "\n" + self._get_sale_order_line_multiline_description_variants()

        return res


    product_attribute_value_ids = fields.Many2many('product.attribute.value', string='Product attributes')
    def _get_sale_order_line_multiline_description_variants(self):
        res1 = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_variants()
        name = ""

        product_attribute_with_is_custom = self.product_custom_attribute_value_ids.mapped('attribute_value_id.attribute_id')

        for attribute_value_with_variant in self.product_attribute_value_ids.filtered(
            lambda ptav: ptav.attribute_id not in product_attribute_with_is_custom
        ):
            if (attribute_value_with_variant.attribute_id.code == "0") or (attribute_value_with_variant.attribute_id.code == "00"):
                name +=""
            name += attribute_value_with_variant.attribute_id.name + ': ' + attribute_value_with_variant.name + "\n"

        # display the no_variant attributes, except those that are also
        # displayed by a custom (avoid duplicate)
        for no_variant_attribute_value in self.product_no_variant_attribute_value_ids.filtered(
            lambda ptav: ptav.attribute_id not in product_attribute_with_is_custom
        ):
            if (no_variant_attribute_value.attribute_id.code == "0") or (no_variant_attribute_value.attribute_id.code == "00"):
                name +=""
            name += no_variant_attribute_value.attribute_id.name + ': ' + no_variant_attribute_value.name + "\n"

        # display the is_custom values
        for pacv in self.product_custom_attribute_value_ids:
            name += pacv.attribute_value_id.attribute_id.name + \
            ': ' + (pacv.custom_value or '').strip() + "\n"

        return name

        return res1            
