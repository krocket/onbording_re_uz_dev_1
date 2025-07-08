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
            # Recherche dans les champs du livre
            book_domain = ['|', '|', '|',
                          ('name', operator, name),
                          ('description', operator, name),
                          ('isbn', operator, name),
                          ('reference', operator, name)]
            
            # Recherche dans les catégories (incluant la hiérarchie)
            category_domain = []
            if name:
                # Chercher les catégories qui correspondent au nom
                categories = self.env['library.book.category'].search([('name', operator, name)])
                if categories:
                    # Inclure les catégories enfants pour chaque catégorie trouvée
                    category_ids = []
                    for category in categories:
                        category_ids.extend(category.search([('id', 'child_of', category.id)]).ids)
                    if category_ids:
                        category_domain = [('category_id', 'in', category_ids)]
            
            # Combiner les domaines
            if category_domain:
                domain = ['|'] + book_domain + category_domain
            else:
                domain = book_domain
                
        return self._search(domain + args, limit=limit)

    @api.model
    def _search(self, args, offset=0, limit=None, order=None):
        # Si on recherche par catégorie, inclure les catégories enfants
        for i, arg in enumerate(args):
            if isinstance(arg, (list, tuple)) and len(arg) == 3:
                field, operator, value = arg
                if field == 'category_id':
                    # Pour tous les opérateurs sur category_id, inclure les enfants
                    if operator in ['=', 'in']:
                        args[i] = ('category_id', 'child_of', value)
                    elif operator == '!=':
                        # Pour l'exclusion, on utilise 'not child_of'
                        args[i] = ('category_id', 'not child_of', value)
                    elif operator == 'not in':
                        # Pour l'exclusion multiple, on utilise 'not child_of' pour chaque valeur
                        if isinstance(value, (list, tuple)):
                            not_conditions = []
                            for val in value:
                                not_conditions.append(('category_id', 'not child_of', val))
                            # Remplacer l'argument actuel par une condition OR de toutes les exclusions
                            args[i] = ('|',) + tuple(not_conditions)
        return super()._search(args, offset=offset, limit=limit, order=order)

