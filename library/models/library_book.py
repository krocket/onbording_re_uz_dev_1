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
        self.button_check_isbn()
                
        
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
                raise UserError(f"ISBN '{book.isbn}' not valid. Please correct the ISBN before saving.")
            if book.isbn and book._check_isbn():
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Validation ISBN',
                        'message': f'ISBN {book.isbn} is valid !',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            return True

    def action_generate_pdf_report(self):
        """Génère un rapport PDF de la liste des livres"""
        # Si appelé depuis le menu ou la liste, générer le rapport pour tous les livres
        if self.env.context.get('action_generate_pdf_report') or len(self) > 1:
            books = self.env['library.book'].search([('active', '=', True)])
            return {
                'type': 'ir.actions.report',
                'report_name': 'library.library_book_report',
                'report_type': 'qweb-pdf',
                'data': None,
                'context': {'doc_ids': books.ids}
            }
        
        # Si appelé depuis un livre spécifique
        return {
            'type': 'ir.actions.report',
            'report_name': 'library.library_book_report',
            'report_type': 'qweb-pdf',
            'data': None,
        }