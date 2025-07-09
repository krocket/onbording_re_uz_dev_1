from odoo import models, fields

class LibraryBook(models.Model):
    _inherit = 'library.book'
    _description = 'Books Inherited'

    price = fields.Float(string='Prix', digits=(10, 2))
    language = fields.Selection([
        ('fr', 'Français'),
        ('en', 'Anglais'),
        ('es', 'Espagnol'),
        ('de', 'Allemand'),
        ('it', 'Italien'),
        ('other', 'Autre')
    ], string='Langue', default='fr')
    isbn = fields.Char(help='International Standard Book Number, 10 digits for ISBN-10, 13 digits for ISBN-13')
    publisher_id = fields.Many2one(index=True)

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(d) for d in self.isbn if d.isdigit()]
        if len(digits) ==  10:
            check = sum(digits[i] * (10 - i) for i in range(10))
            return check % 11 == 0
        else:
            return super()._check_isbn()
        
        
  