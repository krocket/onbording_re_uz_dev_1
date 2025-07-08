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
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
 
}