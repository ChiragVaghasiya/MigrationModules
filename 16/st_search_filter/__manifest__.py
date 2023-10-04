# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Search Filter Extend',
    'version': '16.0.1.0.0',
    'summary': 'Search Filter Extend',
    'sequence': 15,
    'author': 'Surekha Technologies Pvt. Ltd.',
    'description': """
    This module is used for extend search functionality, like it will Save view in searches.
    """,
    'category': 'Hidden/Tools',
    'website': 'https://www.surekhatech.com/',
    'depends': ['web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': ['st_search_filter/static/src/js/*.js',],
    },
    'installable': True,
    'application': False,
    'auto_install': False,  
    'license': 'LGPL-3',
}
