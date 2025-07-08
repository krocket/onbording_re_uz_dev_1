from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Books'

    name = fields.Char(string='Title', required=True)
    publisher_id = fields.Many2one('library.publisher', string='Publisher')
    author_ids = fields.Many2many('library.author', string='Authors')
    description = fields.Text(string='Description')
    publication_date = fields.Date(string='Publication Date')
    isbn = fields.Char(string='ISBN')
    state = fields.Selection([('available', 'Available'), ('borrowed', 'Borrowed'), ('lost', 'Lost')], string='State', default='available')
    loan_date = fields.Date(string='Loan Date')
    return_date = fields.Date(string='Return Date')
    active = fields.Boolean(string='Active', default=True)
    image = fields.Binary(string='Image')
    category_id = fields.Many2one('library.book.category', string='Category')
    reference = fields.Char(string='Reference')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', '|', '|',
                     ('name', operator, name),
                     ('description', operator, name),
                     ('isbn', operator, name),
                     ('reference', operator, name),
                     ('category_id.name', operator, name)]
        return self._search(domain + args, limit=limit)

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        # Si on recherche par catégorie, inclure les catégories enfants
        for i, arg in enumerate(args):
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                field, operator, value = arg
                if field == 'category_id' and operator == '=':
                    # Remplacer par une recherche qui inclut les enfants
                    args[i] = ('category_id', 'child_of', value)
        return super()._search(args, offset=offset, limit=limit, order=order)

