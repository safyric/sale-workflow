# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _get_sale_order_line_multiline_description_sale(self, product):
        res = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_sale(product)
        """ Compute a default multiline description for this sales order line.
        This method exists so it can be overridden in other modules to change how the default name is computed.
        In general only the product is used to compute the name, and this method would not be necessary (we could directly override the method in product).
        BUT in event_sale we need to know specifically the sales order line as well as the product to generate the name:
            the product is not sufficient because we also need to know the event_id and the event_ticket_id (both which belong to the sale order line).
        """
        return product.get_product_multiline_description_sale() + self._get_sale_order_line_multiline_description_variants()
        return res
    
    def _get_sale_order_line_multiline_description_variants(self):
        res1 = super(SaleOrderLine, self)._get_sale_order_line_multiline_description_variants()
        """When using no_variant attributes or is_custom values, the product
        itself is not sufficient to create the description: we need to add
        information about those special attributes and values.
        See note about `product_no_variant_attribute_value_ids` above the field
        definition: this method is not reliable to recompute the description at
        a later time, it should only be used initially.
        :return: the description related to special variant attributes/values
        :rtype: string
        """
        if not self.product_custom_attribute_value_ids and not self.product_no_variant_attribute_value_ids:
            return pacv.attribute_value_id.attribute_id.name 

        name = "\n"

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
