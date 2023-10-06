# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    'name': 'Search Filter Extension',
    'category': 'Hidden/Tools',
    'summary': 'Search Filter Extend',
    'version': '15.0.0.1.0',
    "license": "AGPL-3",
    'description': """
    This module is used for extend search functionality, like it will Save view in searches.
    """,
    'author': 'Aspire Softserv Pvt. Ltd.',
    'website': 'https://www.aspiresoftserv.com/',
    'depends': ['base','web',],
    'assets': {
        'web.assets_backend': ['aspl_search_filter/static/src/js/*.js',],
    },
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support":"odoo@aspiresoftserv.com",
    'images': [
        'static/description/banner.png',
    ],

}
