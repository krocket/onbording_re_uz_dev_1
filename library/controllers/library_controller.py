from odoo import http
from odoo.http import request
import json

class LibraryController(http.Controller):
    
    @http.route('/api/test', type='http', auth='public', methods=['GET'], csrf=False)
    def test_route(self, **kwargs):
        """Route de test simple"""
        try:
            # Vérifier les modèles disponibles
            env = request.env
            models_info = []
            
            # Vérifier library.book
            try:
                book_model = env['library.book']
                book_count = book_model.search_count([])
                models_info.append(f"library.book: {book_count} enregistrements")
            except KeyError:
                models_info.append("library.book: NON DISPONIBLE")
            except Exception as e:
                models_info.append(f"library.book: ERREUR - {str(e)}")
            
            # Vérifier d'autres modèles
            for model_name in ['library.author', 'library.publisher', 'library.book.category']:
                try:
                    model = env[model_name]
                    count = model.search_count([])
                    models_info.append(f"{model_name}: {count} enregistrements")
                except KeyError:
                    models_info.append(f"{model_name}: NON DISPONIBLE")
                except Exception as e:
                    models_info.append(f"{model_name}: ERREUR - {str(e)}")
            
            models_html = "<br>".join(models_info)
            
            return f"""
            <html>
            <head><title>Test API - Diagnostic</title></head>
            <body>
                <h1>API de la bibliothèque - Diagnostic</h1>
                <h2>État des modèles :</h2>
                <p>{models_html}</p>
                <hr>
                <h2>Actions :</h2>
                <ul>
                    <li><a href="/api/books">Tester la liste des livres</a></li>
                    <li><a href="/web#action=library.action_library_book">Ouvrir les livres dans Odoo</a></li>
                </ul>
            </body>
            </html>
            """
        except Exception as e:
            return f"""
            <html>
            <head><title>Erreur de diagnostic</title></head>
            <body>
                <h1>Erreur lors du diagnostic</h1>
                <p>{str(e)}</p>
            </body>
            </html>
            """
    
    @http.route('/api/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books(self, **kwargs):
        """Récupère tous les livres et affiche une vue HTML"""
        try:
            # Vérifier que le modèle existe
            try:
                book_model = request.env['library.book']
            except KeyError:
                return request.render('library.error_template', {
                    'error_message': 'Le modèle library.book n\'est pas disponible. Vérifiez que le module est installé.'
                })
            
            books = book_model.sudo().search([('active', '=', True)])
            
            books_data = []
            for book in books:
                try:
                    book_info = {
                        'id': book.id,
                        'name': book.name or 'Sans titre',
                        'description': book.description or '',
                        'publication_date': book.publication_date.strftime('%Y-%m-%d') if book.publication_date else None,
                        'isbn': book.isbn or '',
                        'state': book.state or 'available',
                        'reference': book.reference or '',
                        'publisher': {
                            'id': book.publisher_id.id,
                            'name': book.publisher_id.name
                        } if book.publisher_id else None,
                        'authors': [{
                            'id': author.id,
                            'name': author.name
                        } for author in book.author_ids if author.name],
                        'category': {
                            'id': book.category_id.id,
                            'name': book.category_id.name
                        } if book.category_id else None
                    }
                    books_data.append(book_info)
                except Exception as book_error:
                    # Ignorer les livres avec des erreurs et continuer
                    continue
            
            # Debug: afficher les données avant le rendu
            print(f"DEBUG: {len(books_data)} livres trouvés")
            for i, book in enumerate(books_data[:3]):  # Afficher les 3 premiers
                print(f"DEBUG: Livre {i+1}: {book.get('name', 'Sans nom')}")
            
            return request.render('library.books_list_template', {
                'books': books_data,
                'title': 'Tous les livres',
                'count': len(books_data)
            })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': f"Erreur lors du chargement des livres: {str(e)}"
            })
    
    @http.route('/api/books/<int:book_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_book(self, book_id, **kwargs):
        """Récupère un livre spécifique et affiche une vue HTML"""
        try:
            book = request.env['library.book'].sudo().browse(book_id)
            
            if not book.exists():
                return request.render('library.error_template', {
                    'error_message': f'Livre avec l\'ID {book_id} non trouvé'
                })
            
            try:
                book_info = {
                    'id': book.id,
                    'name': book.name or 'Sans titre',
                    'description': book.description or '',
                    'publication_date': book.publication_date.strftime('%Y-%m-%d') if book.publication_date else None,
                    'isbn': book.isbn or '',
                    'state': book.state or 'available',
                    'loan_date': book.loan_date.strftime('%Y-%m-%d') if book.loan_date else None,
                    'return_date': book.return_date.strftime('%Y-%m-%d') if book.return_date else None,
                    'reference': book.reference or '',
                    'publisher': {
                        'id': book.publisher_id.id,
                        'name': book.publisher_id.name
                    } if book.publisher_id else None,
                    'authors': [{
                        'id': author.id,
                        'name': author.name
                    } for author in book.author_ids if author.name],
                    'category': {
                        'id': book.category_id.id,
                        'name': book.category_id.name
                    } if book.category_id else None
                }
                
                return request.render('library.book_detail_template', {
                    'book': book_info
                })
                
            except Exception as book_error:
                return request.render('library.error_template', {
                    'error_message': f"Erreur lors du traitement du livre: {str(book_error)}"
                })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': f"Erreur lors du chargement du livre: {str(e)}"
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
                try:
                    book_info = {
                        'id': book.id,
                        'name': book.name or 'Sans titre',
                        'description': book.description or '',
                        'state': book.state or 'available',
                        'isbn': book.isbn or '',
                        'publisher': book.publisher_id.name if book.publisher_id else None,
                        'authors': [author.name for author in book.author_ids if author.name],
                        'category': book.category_id.name if book.category_id else None
                    }
                    books_data.append(book_info)
                except Exception as book_error:
                    # Ignorer les livres avec des erreurs et continuer
                    continue
            
            return request.render('library.books_list_template', {
                'books': books_data,
                'title': f'Résultats de recherche pour "{search_term}"',
                'count': len(books_data),
                'search_term': search_term
            })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': f"Erreur lors de la recherche: {str(e)}"
            }) 