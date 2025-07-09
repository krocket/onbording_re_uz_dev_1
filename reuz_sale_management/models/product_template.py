from odoo import models, fields

class Product(models.Model):
    _inherit = 'product.template'
    _description = 'Product for reuz'

    api_reference = fields.Char(string='API Reference')
    silver_reference = fields.Char(string='Silver Reference')