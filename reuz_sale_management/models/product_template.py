from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product for reuz'

    reuz_format = fields.Char(string='Format')
    reuz_volume = fields.Char(string='Volume')
    reuz_base = fields.Char(string='Base')
    reuz_color = fields.Char(string='Color')
    reuz_technology = fields.Char(string='Technology')

    api_reference = fields.Char(string='API Reference', compute='_compute_api_reference')
    silver_reference = fields.Char(string='Silver Reference')

    @api.depends('reuz_format', 'reuz_volume', 'reuz_base', 'reuz_color', 'reuz_technology')
    def _compute_api_reference(self):
        for record in self:
            record.api_reference = f"{record.reuz_format or ''}{record.reuz_volume or ''}{record.reuz_base or ''}{record.reuz_color or ''}{record.reuz_technology or ''}"
      