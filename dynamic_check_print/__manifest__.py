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
    'website': 'https://apps.odoo.com/apps/modules/browse?author=ACH%20Alchemical%20Code',
    'license': 'OPL-1',
    'price': 36.95,
    'currency': 'USD',
    'support': 'mikealquimia@gmail.com',
    'category': 'Accounting/Payment',
    'version': '19.0.1.0.0',
    'data': [
        'security/dynamic_check_print.xml',
        'security/ir.model.access.csv',
        'views/account_journal.xml',
        'views/format_checkprint.xml',
        'views/account_payment.xml',
    ],
    'images': ['static/description/banner.gif'],
    'depends': ['account', 'account_check_printing'],
}