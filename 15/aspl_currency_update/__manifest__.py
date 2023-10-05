# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Currency Rate Update",
    "category": "Accounting",
    "summary": "Update exchange rates from Exchangereates(APILayer)",
    "version": "15.0.0.1.0",
    "license": "AGPL-3",
    'description': """
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['base', 'account'],
    "data": [
        'data/currency_rates_updation.xml',
        'views/res_config_settings.xml',
        'views/res_currency.xml',
    ],
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support":"odoo@aspiresoftserv.com",
}