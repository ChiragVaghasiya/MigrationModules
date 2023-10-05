# -*- coding: utf-8 -*-

{
    'name': "Aspl Attendance WFH",

    'description': """
        Aspire Attendance WFH
    """,
    'author': "Aspire Softserv Private Limited",
    'website': "http://www.aspiresoftware.in",
    'category': 'Attendance',
    'version': '15.0.0.0.4',
    'depends': ['base', 'hr', 'hr_attendance'],
    'data': [
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'data/work_from_home_mail.xml',
        'data/attnedance_work_from_home.xml',
        'views/inherit_hr_employee_view.xml',
        'views/attendance_work_from_home_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
    "installable": True,
    "support": "odoo@aspiresoftserv.com",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
