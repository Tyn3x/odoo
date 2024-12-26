# -*- coding: utf-8 -*-
{
    'name': "estate_account",

    'summary': "Link the estate an account modules",

    'description': """
        Link the estate an account modules
    """,

    'author': "Martin Ferreira",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['estate', 'account'],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    'application': 'True',
}

