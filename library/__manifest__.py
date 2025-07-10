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
    'depends': [],
    'data': [
        'views/library_menu.xml',
        'views/book_view.xml',
        'views/category_view.xml',
        'views/author_view.xml',
        'views/publisher_view.xml',
        'data/categories.xml',
        'data/authors.xml',
        'data/publisher.xml',
        'data/report_actions.xml',
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'reports/library_book_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
 
}