# -*- coding: utf-8 -*-

from odoo import api, models
from odoo.exceptions import UserError


class LibraryBookReport(models.AbstractModel):
    _name = 'report.library.library_book_report'
    _description = 'Rapport des livres de bibliothèque'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Récupère les données pour le rapport"""
        docs = self.env['library.book'].browse(docids)
        
        # Récupérer tous les livres si aucun ID spécifique
        if not docids:
            docs = self.env['library.book'].search([('active', '=', True)])
        
        # Préparer les données pour le template
        books_data = []
        for book in docs:
            authors = ', '.join([author.name for author in book.author_ids]) if book.author_ids else 'Non spécifié'
            publisher = book.publisher_id.name if book.publisher_id else 'Non spécifié'
            category = book.category_id.name if book.category_id else 'Non spécifié'
            
            books_data.append({
                'name': book.name,
                'description': book.description or '',
                'isbn': book.isbn or 'Non spécifié',
                'publication_date': book.publication_date.strftime('%d/%m/%Y') if book.publication_date else 'Non spécifié',
                'state': dict(book._fields['state'].selection).get(book.state, book.state),
                'authors': authors,
                'publisher': publisher,
                'category': category,
                'reference': book.reference or 'Non spécifié',
            })
        
        return {
            'doc_ids': docids,
            'doc_model': 'library.book',
            'docs': docs,
            'books_data': books_data,
            'total_books': len(books_data),
            'available_books': len([b for b in books_data if b['state'] == 'Disponible']),
            'borrowed_books': len([b for b in books_data if b['state'] == 'Emprunté']),
            'lost_books': len([b for b in books_data if b['state'] == 'Perdu']),
        } 