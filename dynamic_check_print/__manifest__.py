# -*- coding: utf-8 -*-
{
    'name': "Check Printing Format",
    'summary': """Scan your check and adjust it to be printed""",
    'description': """
        Add signature field in Alborán depending on validation in Stock Picking type, which is printed in Stock Picking report
    """,
    'author': "Gt Alchemy Development",
    'license': 'LGPL-3',
    'price': 35.00,
    'currency': 'USD',
    'support': 'developmentalchemygx@gmail.com',
    'category': 'Account',
    'version': '15.1.1',
    'data': [
        'security/dynamic_check_print.xml',
        'security/ir.model.access.csv',
        'views/account_journal.xml',
        'views/format_checkprint.xml',
    ],
    'images': ['static/description/banner.png'],
    'depends': ['account', 'account_check_printing'],
}