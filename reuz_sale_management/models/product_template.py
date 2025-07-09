from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product for reuz'

    format = fields.Char(string='Format')
    volume = fields.Char(string='Volume')
    base = fields.Char(string='Base')
    color = fields.Char(string='Color')
    technology = fields.Char(string='Technology')

    api_reference = fields.Char(string='API Reference', compute='_compute_api_reference')
    silver_reference = fields.Char(string='Silver Reference')

    @api.depends('format', 'volume', 'base', 'color', 'technology')
    def _compute_api_reference(self):
        for record in self:
            record.api_reference = f"{record.format}{record.volume}{record.base}{record.color}{record.technology}"