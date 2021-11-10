# -*- coding: utf-8 -*-
{
    'name': "[SALES] Fix Down Payment Lines",
    'summary': "This module will fix the problem of creating only one down payment line in the invoice & sale order.",
    'description': "This module will fix the problem of creating only one down payment line in the invoice & sale order.",
    'author': "Sayed Ahmed Abbas",
    'category': 'Sales/Sales',
    'version': '0.1',
    'depends': ['sale', 'stock'],
    'data': [
        'views/sale_order_inherit.xml',
    ],
}
