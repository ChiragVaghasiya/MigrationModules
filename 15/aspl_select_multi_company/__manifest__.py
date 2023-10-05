# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Multi Company Selection",
    "category": "Base",
    "summary": "Multi Company Selection",
    "version": "15.0.0.1.0",
    "license": "AGPL-3",
    'description': """
        Set All company to enable at login time, and user can select and deselect company later.
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['web'],
    'assets': {
        'web.assets_backend': [
            'aspl_select_multi_company/static/src/js/company_service.js',
            'aspl_select_multi_company/static/src/js/switch_company_menu.js'
        ],
    },
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support":"odoo@aspiresoftserv.com",
}