{
    'name': 'Trade Management',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom extension for trading company',
    'author': 'Fatma Salim',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}