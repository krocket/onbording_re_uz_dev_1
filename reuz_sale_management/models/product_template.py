from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product for reuz'

    reuz_product_format = fields.Char(string='Format')
    reuz_product_volume = fields.Char(string='Volume')
    reuz_product_base = fields.Char(string='Base')
    reuz_product_color = fields.Char(string='Color')
    reuz_product_technology = fields.Char(string='Technology')

    reuz_api_reference = fields.Char(string='API Reference', compute='_compute_api_reference')
    reuz_silver_reference = fields.Char(string='Silver Reference')

    @api.depends('reuz_product_format', 'reuz_product_volume', 'reuz_product_base', 'reuz_product_color', 'reuz_product_technology')
    def _compute_api_reference(self):
        for record in self:
            record.reuz_api_reference = f"{record.reuz_product_format or ''}{record.reuz_product_volume or ''}{record.reuz_product_base or ''}{record.reuz_product_color or ''}{record.reuz_product_technology or ''}"
      