# -*- coding: utf-8 -*-
{
    'name': "Check Printing Format",
    'summary': """Scan your check and adjust it to be printed
    Crea y configura cheques para imprimir desde Odoo
    Create and configure checks to print from Odoo
    Créer et configurer des chèques à imprimer depuis Odoo
    """,
    'description': """
        Scan your check and adjust it to be printed
    Crea y configura cheques para imprimir desde Odoo
    Create and configure checks to print from Odoo
    Créer et configurer des chèques à imprimer depuis Odoo
    """,
    'author': "ACH Alchemical Code",
    'live_test_url': 'https://youtu.be/QsPxF8xqlUw',
    'license': 'LGPL-3',
    'price': 35.00,
    'currency': 'USD',
    'support': 'developmentalchemygx@gmail.com',
    'category': 'Account',
    'version': '15.2.1',
    'data': [
        'security/dynamic_check_print.xml',
        'security/ir.model.access.csv',
        'views/account_journal.xml',
        'views/format_checkprint.xml',
    ],
    'images': ['static/description/banner.gif'],
    'depends': ['account', 'account_check_printing'],
}