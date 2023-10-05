# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Aspire Biometric Attendance",
    "category": "Attendance",
    "summary": "Attendance Biometric Modules",
    "version": "16.0.0.1.0",
    "license": "AGPL-3",
    'description': """
        Synchronization with ESSL to get employee's every day attendances.
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ['base', 'hr', 'hr_attendance'],
    "data": [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'data/attendance_log_cron.xml',
        'views/hr_attendance_views.xml',
        'views/attendance_log_view.xml',
        'views/connector_setup.xml',
        'views/inherit_hr_employee_view.xml',
    ],
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
