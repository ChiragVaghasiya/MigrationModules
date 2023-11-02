# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Automatic Lead Followup",
    "category": "CRM",
    "summary": "",
    "version": "15.0.0.1.0",
    "price": 0.00,
    "license": "AGPL-3",
    'description': """
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['base', 'hr', 'crm', 'mail'],
    "external_dependencies": {
        'python': ['html']
    },
    "data": [
        'security/ir.model.access.csv',
        'data/followup_schedular.xml',
        'views/crm_followup_view.xml',
        'views/crm_lead_view.xml',
    ],
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
    # 'images': ['static/description/banner.gif'],
}
