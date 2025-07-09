{
    'name': 'Vente de livres',
    'version': '18.0.1.0',
    'category': 'Education',
    'summary': 'Module de vente de livres pour Odoo',
    'description': """
        Module de vente de livres pour Odoo
    """,
    'author': 'Coco',
    'license': 'LGPL-3',
    'depends': ['library'],
    'data': [
        'views/book_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
 
}