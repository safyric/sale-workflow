# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    short_name = fields.Char(string='Value', required=True, translate=True)
