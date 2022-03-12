# -*- coding: utf-8 -*-
{
    'name': "Check Printing Format",
    'summary': """Scan your check and adjust it to be printed""",
    'description': """
        Add signature field in Alborán depending on validation in Stock Picking type, which is printed in Stock Picking report
    """,
    'author': "Gt Alchemy Development",
    'license': 'LGPL-3',
    'support': 'developmentalchemygx@gmail.com',
    'category': 'Account',
    'version': '15.1.1',
    'data': [
        'views/account_payment.xml',
        #'reports/report_picking.xml',
    ],
    'images': ['static/description/banner.png'],
    'depends': ['account_check_printing'],
}