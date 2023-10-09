# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    'name': 'Save View to favourite',
    'category': 'Hidden/Tools',
    'summary': 'Get the view loaded as is the way you marked it favourite.',
    'version': '16.0.0.1.0',
    "license": "AGPL-3",
    'description': """
        In Odoo, when you filter/group data and save it as favorites, Odoo doesn't remember the view name. This module loads the same view & grouping as you had while saving it as favorite.
    """,
    'author': 'Aspire Softserv Pvt. Ltd.',
    'website': 'https://www.aspiresoftserv.com/',
    'depends': ['base','web',],
    'assets': {
        'web.assets_backend': ['aspl_save_view_to_favourite/static/src/js/*.js',],
    },
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support":"odoo@aspiresoftserv.com",
    "images": ['static/description/banner.gif'],
}
