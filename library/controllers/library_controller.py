from odoo import http
from odoo.http import request
import json

class LibraryController(http.Controller):
    
    @http.route('/api/test', type='http', auth='public', methods=['GET'], csrf=False)
    def test_route(self, **kwargs):
        """Route de test simple"""
        return """
        <html>
        <head><title>Test API</title></head>
        <body>
            <h1>API de la bibliothèque fonctionne !</h1>
            <p>Le contrôleur est correctement chargé.</p>
            <a href="/api/books">Voir tous les livres</a>
        </body>
        </html>
        """
    
    @http.route('/api/books', type='http', auth='public', methods=['GET'], csrf=False)
    def get_books(self, **kwargs):
        """Récupère tous les livres et affiche une vue HTML"""
        try:
            # Vérifier que le modèle existe
            if not request.env.get('library.book'):
                return """
                <html>
                <head><title>Erreur</title></head>
                <body>
                    <h1>Erreur</h1>
                    <p>Le modèle library.book n'est pas disponible.</p>
                </body>
                </html>
                """
            
            books = request.env['library.book'].sudo().search([('active', '=', True)])
            
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
            
            # Rendu simple en HTML pour éviter les problèmes de template
            html_content = f"""
            <html>
            <head>
                <title>Bibliothèque - Tous les livres</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-4">
                    <h1>Bibliothèque - Tous les livres</h1>
                    <p>Nombre de livres: {len(books_data)}</p>
                    
                    <form method="GET" action="/api/books/search" class="mb-4">
                        <div class="input-group">
                            <input type="text" name="q" class="form-control" placeholder="Rechercher...">
                            <button class="btn btn-primary" type="submit">Rechercher</button>
                        </div>
                    </form>
                    
                    <div class="row">
            """
            
            for book in books_data:
                state_class = 'success' if book['state'] == 'available' else 'warning' if book['state'] == 'borrowed' else 'danger'
                authors = ', '.join([author['name'] for author in book['authors']]) if book['authors'] else 'Auteur inconnu'
                category = book['category']['name'] if book['category'] else 'Catégorie inconnue'
                publisher = book['publisher']['name'] if book['publisher'] else 'Éditeur inconnu'
                
                html_content += f"""
                        <div class="col-md-4 mb-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">{book['name']}</h5>
                                    <span class="badge bg-{state_class} mb-2">{book['state']}</span>
                                    <p class="card-text"><strong>Auteurs:</strong> {authors}</p>
                                    <p class="card-text"><strong>Catégorie:</strong> {category}</p>
                                    <p class="card-text"><strong>Éditeur:</strong> {publisher}</p>
                                    {f'<p class="card-text"><strong>ISBN:</strong> {book["isbn"]}</p>' if book['isbn'] else ''}
                                    <a href="/api/books/{book['id']}" class="btn btn-primary btn-sm">Voir détails</a>
                                </div>
                            </div>
                        </div>
                """
            
            html_content += """
                    </div>
                </div>
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
                <p>Erreur lors du chargement des livres: {str(e)}</p>
                <a href="/api/test">Retour au test</a>
            </body>
            </html>
            """
    
    @http.route('/api/books/<int:book_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_book(self, book_id, **kwargs):
        """Récupère un livre spécifique et affiche une vue HTML"""
        try:
            book = request.env['library.book'].sudo().browse(book_id)
            
            if not book.exists():
                return f"""
                <html>
                <head><title>Livre non trouvé</title></head>
                <body>
                    <h1>Livre non trouvé</h1>
                    <p>Le livre avec l'ID {book_id} n'existe pas.</p>
                    <a href="/api/books">Retour à la liste</a>
                </body>
                </html>
                """
            
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
                
                state_class = 'success' if book_info['state'] == 'available' else 'warning' if book_info['state'] == 'borrowed' else 'danger'
                authors = ', '.join([author['name'] for author in book_info['authors']]) if book_info['authors'] else 'Auteur inconnu'
                category = book_info['category']['name'] if book_info['category'] else 'Catégorie inconnue'
                publisher = book_info['publisher']['name'] if book_info['publisher'] else 'Éditeur inconnu'
                
                html_content = f"""
                <html>
                <head>
                    <title>Détails du livre - {book_info['name']}</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                </head>
                <body>
                    <div class="container mt-4">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h1>Détails du livre</h1>
                            <a href="/api/books" class="btn btn-outline-primary">← Retour à la liste</a>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-8">
                                <div class="card">
                                    <div class="card-body">
                                        <h2 class="card-title">{book_info['name']}</h2>
                                        <span class="badge bg-{state_class} mb-3">{book_info['state']}</span>
                                        
                                        {f'<h5>Description</h5><p>{book_info["description"]}</p>' if book_info['description'] else ''}
                                        
                                        <h5>Informations</h5>
                                        <ul class="list-unstyled">
                                            <li><strong>Auteurs:</strong> {authors}</li>
                                            <li><strong>Catégorie:</strong> {category}</li>
                                            <li><strong>Éditeur:</strong> {publisher}</li>
                                            {f'<li><strong>ISBN:</strong> {book_info["isbn"]}</li>' if book_info['isbn'] else ''}
                                            {f'<li><strong>Date de publication:</strong> {book_info["publication_date"]}</li>' if book_info['publication_date'] else ''}
                                            {f'<li><strong>Date d\'emprunt:</strong> {book_info["loan_date"]}</li>' if book_info['loan_date'] else ''}
                                            {f'<li><strong>Date de retour:</strong> {book_info["return_date"]}</li>' if book_info['return_date'] else ''}
                                            {f'<li><strong>Référence:</strong> {book_info["reference"]}</li>' if book_info['reference'] else ''}
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                return html_content
                
            except Exception as book_error:
                return f"""
                <html>
                <head><title>Erreur</title></head>
                <body>
                    <h1>Erreur</h1>
                    <p>Erreur lors du traitement du livre: {str(book_error)}</p>
                    <a href="/api/books">Retour à la liste</a>
                </body>
                </html>
                """
            
        except Exception as e:
            return f"""
            <html>
            <head><title>Erreur</title></head>
            <body>
                <h1>Erreur</h1>
                <p>Erreur lors du chargement du livre: {str(e)}</p>
                <a href="/api/books">Retour à la liste</a>
            </body>
            </html>
            """
    
    @http.route('/api/books/search', type='http', auth='public', methods=['GET'], csrf=False)
    def search_books(self, **kwargs):
        """Recherche des livres et affiche une vue HTML"""
        try:
            search_term = kwargs.get('q', '')
            if not search_term:
                return """
                <html>
                <head><title>Erreur</title></head>
                <body>
                    <h1>Erreur</h1>
                    <p>Terme de recherche requis</p>
                    <a href="/api/books">Retour à la liste</a>
                </body>
                </html>
                """
            
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
            
            html_content = f"""
            <html>
            <head>
                <title>Résultats de recherche</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            </head>
            <body>
                <div class="container mt-4">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h1>Résultats de recherche pour "{search_term}"</h1>
                        <a href="/api/books" class="btn btn-outline-primary">← Retour à la liste</a>
                    </div>
                    
                    <p>Nombre de résultats: {len(books_data)}</p>
                    
                    <form method="GET" action="/api/books/search" class="mb-4">
                        <div class="input-group">
                            <input type="text" name="q" class="form-control" placeholder="Rechercher..." value="{search_term}">
                            <button class="btn btn-primary" type="submit">Rechercher</button>
                        </div>
                    </form>
                    
                    <div class="row">
            """
            
            for book in books_data:
                state_class = 'success' if book['state'] == 'available' else 'warning' if book['state'] == 'borrowed' else 'danger'
                authors = ', '.join(book['authors']) if book['authors'] else 'Auteur inconnu'
                category = book['category'] or 'Catégorie inconnue'
                publisher = book['publisher'] or 'Éditeur inconnu'
                
                html_content += f"""
                        <div class="col-md-4 mb-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">{book['name']}</h5>
                                    <span class="badge bg-{state_class} mb-2">{book['state']}</span>
                                    <p class="card-text"><strong>Auteurs:</strong> {authors}</p>
                                    <p class="card-text"><strong>Catégorie:</strong> {category}</p>
                                    <p class="card-text"><strong>Éditeur:</strong> {publisher}</p>
                                    {f'<p class="card-text"><strong>ISBN:</strong> {book["isbn"]}</p>' if book['isbn'] else ''}
                                    <a href="/api/books/{book['id']}" class="btn btn-primary btn-sm">Voir détails</a>
                                </div>
                            </div>
                        </div>
                """
            
            html_content += """
                    </div>
                </div>
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
                <p>Erreur lors de la recherche: {str(e)}</p>
                <a href="/api/books">Retour à la liste</a>
            </body>
            </html>
            """ 