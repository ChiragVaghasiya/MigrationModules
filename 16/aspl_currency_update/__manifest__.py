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
    "summary": "Update currencies with live rates using ExachangeRatesAPIs.",
    "version": "16.0.0.1.0",
    "license": "AGPL-3",
    'description': """
        This module helps you to keep track of live currency rates using Exchange Rate APIs(put a link to website). Generate an API key from Exchange Rate APIs portal by simply registering to it and configure it in settings. You are all done!!
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
    "images": ['static/description/banner.gif'],
}