# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Aspl Attendance WFH",
    "category": "Attendance",
    "summary": "Attendance WFH Modules",
    "version": "15.0.0.1.0",
    "license": "AGPL-3",
    'description': """
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['base', 'hr', 'hr_attendance'],
    "data": [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'data/work_from_home_mail.xml',
        'data/attnedance_work_from_home.xml',
        'views/inherit_hr_employee_view.xml',
        'views/attendance_work_from_home_view.xml',
    ],
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
