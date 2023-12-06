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
    "summary": "Odoo automates lead nurturing for improved sales efficiency.",
    "version": "16.0.0.1.0",
    "price": 0.00,
    "license": "AGPL-3",
    'description': """
        This module in Odoo automates the process of following up with leads and potential customers. It allows you to set predefined rules and schedules for follow-up actions, ensuring that leads are nurtured and converted into customers more efficiently. This module helps streamline sales processes and improve lead conversion rates.
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['hr', 'crm', 'mail'],
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
    "images": ['static/description/banner.gif'],
}
