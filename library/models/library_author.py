from odoo import models, fields, api

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Authors'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    biography = fields.Text(string='Biography')
    birth_date = fields.Date(string='Birth Date')
    death_date = fields.Date(string='Death Date')
    nationality = fields.Char(string='Nationality')
    website = fields.Char(string='Website')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    active = fields.Boolean(string='Active', default=True)
    image = fields.Binary(string='Photo')
    
 