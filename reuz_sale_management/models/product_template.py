from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product for reuz'

    product_format = fields.Char(string='Format')
    product_volume = fields.Char(string='Volume')
    product_base = fields.Char(string='Base')
    product_color = fields.Char(string='Color')
    product_technology = fields.Char(string='Technology')

    api_reference = fields.Char(string='API Reference', compute='_compute_api_reference')
    silver_reference = fields.Char(string='Silver Reference')

    @api.depends('product_format', 'product_volume', 'product_base', 'product_color', 'product_technology')
    def _compute_api_reference(self):
        for record in self:
            record.api_reference = f"{record.product_format or ''}{record.product_volume or ''}{record.product_base or ''}{record.product_color or ''}{record.product_technology or ''}"
      