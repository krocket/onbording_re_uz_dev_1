from odoo import models, fields, api
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Books'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    publication_date = fields.Date(string='Publication Date')
    isbn = fields.Char(string='ISBN')
    state = fields.Selection([('available', 'Available'), ('borrowed', 'Borrowed'), ('lost', 'Lost')], string='State', default='available')
    loan_date = fields.Date(string='Loan Date')
    return_date = fields.Date(string='Return Date')
    active = fields.Boolean(string='Active', default=True)
    image = fields.Binary(string='Image')
    reference = fields.Char(string='Reference')


    # Restrictions fields
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    author_ids = fields.Many2many('library.author', string='Authors')
    category_id = fields.Many2one('library.book.category', string='Category')
   
    @api.constrains('isbn')
    def _check_isbn_constraint(self):
        for record in self:
            if record.isbn:
                try:
                    record.button_check_isbn()
                except UserError as e:
                    raise UserError(str(e))

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(d) for d in self.isbn if d.isdigit()]
        if len(digits) != 13:
            return False
        check = sum(digits[i] * (1 if i % 2 == 0 else 3) for i in range(13))
        return check % 10 == 0

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise UserError("ISBN is required")
            if book.isbn and not book._check_isbn():
                raise UserError("ISBN is not valid")
            if book.isbn and book._check_isbn() == True:
                raise UserError("ISBN is valid")


