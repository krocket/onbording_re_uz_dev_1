{
    'name': 'Gestion de Bibliothèque',
    'version': '18.0.1.0',
    'category': 'Education',
    'summary': 'Module de gestion de bibliothèque pour Odoo',
    'description': """
        Module de gestion de bibliothèque pour Odoo
    """,
    'author': 'Coco',
    'license': 'LGPL-3',
    'depends': ["website"],
    'data': [
        # Menus
        'views/menus/library_menu.xml',
        
        # Vues web classiques
        'views/web/book_view.xml',
        'views/web/category_view.xml',
        'views/web/author_view.xml',
        'views/web/publisher_view.xml',
        
        # Vues API
        'views/api/books_api_view.xml',
        'views/api/book_detail_view.xml',
        'views/api/error_view.xml',
        'views/api/modern_interface_view.xml',
        
        # Données
        'data/categories.xml',
        'data/authors.xml',
        'data/publisher.xml',
        'data/report_actions.xml',
        
        # Sécurité
        'security/library_security.xml',
        'security/ir.model.access.csv',
        
        # Rapports
        'reports/library_book_report.xml',
        'reports/library_book_detail_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}