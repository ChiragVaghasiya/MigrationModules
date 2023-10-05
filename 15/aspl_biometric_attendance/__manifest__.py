# -*- coding: utf-8 -*-

{
    'name': "Aspire Biometric Attendance",

    'description': """
        Aspire Biometric Attendance
    """,
    'author': "Aspire Softserv Private Limited",
    'website': "http://www.aspiresoftware.in",
    'category': 'Attendance',
    'version': '15.0.0.0.4',
    'license': 'LGPL-3',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'data/attendance_log_cron.xml',
        'views/hr_attendance_views.xml',
        'views/attendance_log_view.xml',
        'views/connector_setup.xml',
        'views/inherit_hr_employee_view.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
