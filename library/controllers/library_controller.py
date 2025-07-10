from odoo import http
from odoo.http import request
import json

class LibraryController(http.Controller):
    
    @http.route('/api/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books(self, **kwargs):
        """Récupère tous les livres et affiche une vue HTML"""
        try:
            books = request.env['library.book'].sudo().search([('active', '=', True)])
            
            books_data = []
            for book in books:
                book_info = {
                    'id': book.id,
                    'name': book.name,
                    'description': book.description,
                    'publication_date': book.publication_date.strftime('%Y-%m-%d') if book.publication_date else None,
                    'isbn': book.isbn,
                    'state': book.state,
                    'reference': book.reference,
                    'publisher': {
                        'id': book.publisher_id.id,
                        'name': book.publisher_id.name
                    } if book.publisher_id else None,
                    'authors': [{
                        'id': author.id,
                        'name': author.name
                    } for author in book.author_ids],
                    'category': {
                        'id': book.category_id.id,
                        'name': book.category_id.name
                    } if book.category_id else None
                }
                books_data.append(book_info)
            
            return request.render('library.books_list_template', {
                'books': books_data,
                'title': 'Tous les livres',
                'count': len(books_data)
            })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': str(e)
            })
    
    @http.route('/api/books/<int:book_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_book(self, book_id, **kwargs):
        """Récupère un livre spécifique et affiche une vue HTML"""
        try:
            book = request.env['library.book'].sudo().browse(book_id)
            
            if not book.exists():
                return request.render('library.error_template', {
                    'error_message': 'Livre non trouvé'
                })
            
            book_info = {
                'id': book.id,
                'name': book.name,
                'description': book.description,
                'publication_date': book.publication_date.strftime('%Y-%m-%d') if book.publication_date else None,
                'isbn': book.isbn,
                'state': book.state,
                'loan_date': book.loan_date.strftime('%Y-%m-%d') if book.loan_date else None,
                'return_date': book.return_date.strftime('%Y-%m-%d') if book.return_date else None,
                'reference': book.reference,
                'publisher': {
                    'id': book.publisher_id.id,
                    'name': book.publisher_id.name
                } if book.publisher_id else None,
                'authors': [{
                    'id': author.id,
                    'name': author.name
                } for author in book.author_ids],
                'category': {
                    'id': book.category_id.id,
                    'name': book.category_id.name
                } if book.category_id else None
            }
            
            return request.render('library.book_detail_template', {
                'book': book_info
            })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': str(e)
            })
    
    @http.route('/api/books/search', type='http', auth='public', methods=['GET'], csrf=False)
    def search_books(self, **kwargs):
        """Recherche des livres et affiche une vue HTML"""
        try:
            search_term = kwargs.get('q', '')
            if not search_term:
                return request.render('library.error_template', {
                    'error_message': 'Terme de recherche requis'
                })
            
            domain = [
                ('active', '=', True),
                '|', '|', '|',
                ('name', 'ilike', search_term),
                ('author_ids.name', 'ilike', search_term),
                ('category_id.name', 'ilike', search_term),
                ('publisher_id.name', 'ilike', search_term)
            ]
            
            books = request.env['library.book'].sudo().search(domain)
            
            books_data = []
            for book in books:
                book_info = {
                    'id': book.id,
                    'name': book.name,
                    'description': book.description,
                    'state': book.state,
                    'isbn': book.isbn,
                    'publisher': book.publisher_id.name if book.publisher_id else None,
                    'authors': [author.name for author in book.author_ids],
                    'category': book.category_id.name if book.category_id else None
                }
                books_data.append(book_info)
            
            return request.render('library.books_list_template', {
                'books': books_data,
                'title': f'Résultats de recherche pour "{search_term}"',
                'count': len(books_data),
                'search_term': search_term
            })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': str(e)
            }) 