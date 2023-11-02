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
    "license": "AGPL-3",
    "price": 0.00,
    'description': """
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['base','crm', 'mail', 'mail_tracking'],
    "data": [
        'security/ir.model.access.csv',
        'data/followup_schedular.xml',
        'views/crm_views.xml',
        'views/blocked_emails.xml',
        'views/crm_lead.xml',
        'views/crm_followup_view.xml',
        'views/crm_industry_view.xml',
    ],
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support":"odoo@aspiresoftserv.com",
}