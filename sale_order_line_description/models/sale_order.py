
# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_long_description = fields.Boolean('Order Line Long Description', help="Is true if the sales order line is long full description.")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    @api.multi
    def get_sale_order_line_multiline_description_sale(self, product):
        res = super(SaleOrderLine,self).get_sale_order_line_multiline_description_sale(product)
        if product.description_sale:
            return product.display_name \
                + "\n" + self._get_sale_order_line_multiline_description_variants() \
                + product.description_sale
        return product.display_name \
            + "\n" + self._get_sale_order_line_multiline_description_variants().strip(', ')

        return res


    product_attribute_value_ids = fields.Many2many('product.attribute.value', string='Product attributes')
    def _get_sale_order_line_multiline_description_variants(self):
        res1 = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_variants()
        name = ""

        product_attribute_with_is_custom = self.product_custom_attribute_value_ids.mapped('attribute_value_id.attribute_id')


        for attribute_value_with_variant in self.product_attribute_value_ids.filtered(
                lambda ptav: ptav.attribute_id not in product_attribute_with_is_custom
            ):
            if self.order_id.is_long_description:
                if no_variant_attribute_value.attribute_id.description and no_variant_attribute_value.attribute_id.is_reverse_description == False:
                    name += no_variant_attribute_value.name + " " + no_variant_attribute_value.attribute_id.description + ", "
                elif no_variant_attribute_value.attribute_id.description and no_variant_attribute_value.attribute_id.is_reverse_description == True:
                    name += no_variant_attribute_value.attribute_id.description + " " + no_variant_attribute_value.name + ", "
                else:
                    name += no_variant_attribute_value.name + ", "
            else:
                name += no_variant_attribute_value.attribute_id.name + ': ' + no_variant_attribute_value.name + "\n"

        # display the is_custom values
        for pacv in self.product_custom_attribute_value_ids:
            if self.order_id.is_long_description:
                if pacv.attribute_value_id.description and pacv.attribute_value_id.is_reverse_description == False:
                    name += (pacv.custom_value or '').strip() + " " + pacv.attribute_value_id.attribute_id.name + ", "
                elif pacv.attribute_value_id.description and pacv.attribute_value_id.is_reverse_description == True:
                    name += pacv.attribute_value_id.attribute_id.name + " " + (pacv.custom_value or '').strip() + ", "
                else:
                    name += (pacv.custom_value or '').strip() + ", "
            else:
                name += pacv.attribute_value_id.attribute_id.name + \
                    ': ' + (pacv.custom_value or '').strip() + "\n"

        return name

        return res1
