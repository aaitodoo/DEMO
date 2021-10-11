# -*- coding: utf-8 -*-
{
    'name': "Electronic invoice KSA - phase 1 (QR Code)",

    'summary': """
      Electronic invoice KSA - phase 1 (QR Code)""",

    'description': """
        Electronic invoice KSA - phase 1 (QR Code)
    """,

    'author': "Awamer Alsahabka Digital Solutions",
    'website': "http://aait.sa",

    'category': 'accounting',
    'version': '0.1',
    #'price': 19.0,  
    #'currency': 'USD',
    'depends': ['base', 'account', 'sale', 'purchase'],

    'data': [
        'views/views.xml',
        'reports/invoice_inherit_report.xml',
    ],
}
