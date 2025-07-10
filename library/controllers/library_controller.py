from odoo import http
from odoo.http import request

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
                    <li><a href="/api/books-simple">Tester la version simple</a></li>
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
    
    @http.route('/api/books-simple', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books_simple(self, **kwargs):
        """Version très simple pour tester"""
        try:
            books = request.env['library.book'].sudo().search([])
            
            html_content = """
            <html>
            <head><title>Livres - Version Simple</title></head>
            <body>
                <h1>Liste des livres (Version Simple)</h1>
                <p>Nombre de livres trouvés: """ + str(len(books)) + """</p>
                <ul>
            """
            
            for book in books:
                html_content += f"<li>{book.name or 'Sans titre'} (ID: {book.id})</li>"
            
            html_content += """
                </ul>
                <p><a href="/api/test">Retour au diagnostic</a></p>
            </body>
            </html>
            """
            
            return html_content
            
        except Exception as e:
            return f"""
            <html>
            <head><title>Erreur</title></head>
            <body>
                <h1>Erreur</h1>
                <p>{str(e)}</p>
                <p><a href="/api/test">Retour au diagnostic</a></p>
            </body>
            </html>
            """
    
    @http.route('/api/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books(self, **kwargs):
        """Récupère tous les livres et affiche une vue HTML"""
        try:
            books = request.env['library.book'].sudo().search([])
            
            books_data = []
            for book in books:
                book_info = {
                    'id': book.id,
                    'name': book.name or 'Sans titre',
                    'state': book.state or 'available'
                }
                books_data.append(book_info)
            
            return request.render('library.books_list_template', {
                'books': books_data,
                'title': 'Tous les livres',
                'count': len(books_data)
            })
            
        except Exception as e:
            return request.render('library.error_template', {
                'error_message': f"Erreur lors du chargement des livres: {str(e)}"
            }) 