from odoo import models, fields, api

class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Publishers'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    founded_date = fields.Date(string='Founded Date')
    website = fields.Char(string='Website')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    country_id = fields.Many2one('res.country', string='Country')
    active = fields.Boolean(string='Active', default=True)
    logo = fields.Binary(string='Logo')
    
