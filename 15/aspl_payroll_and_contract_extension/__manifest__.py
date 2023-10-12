# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Aspire Payroll and Contract Extension",
    "category": "Payroll",
    "summary": "",
    "version": "16.0.0.1.0",
    "license": "AGPL-3",
    'description': """
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": [
                'base',
                'hr',
                'hr_contract',
                'hr_holidays',
                'hr_payroll_community',
                'hr_attendance',
                'mail',
                ],
    "external_dependencies": {
        'python': [
            'bs4', 'xlsxwriter', 'fiscalyear', 'openpyxl'
        ]},
    "data": [
        'security/ir.model.access.csv',
        'security/custom_payslip_security.xml',
        'data/payslip_mail_data.xml',
        'data/salary_rule_data.xml',
        'data/salary_structure.xml',
        'views/hr_employee_view.xml',
        'views/contract_config_view.xml',
        'views/payroll_config_view.xml',
        'views/tax_calculations_view.xml',
        'views/it_declaration_schedule.xml',
        'views/it_statement_views.xml',
        'views/hr_payslip_batch_view.xml',
        'views/employee_full_final_view.xml',
        'wizards/payslip_wizard_view.xml',
        'wizards/attendance_shortfall_wizard_view.xml',
        'views/payslip_modification.xml',
        'views/res_company_payroll_configuration.xml',
        'reports/employee_full_and_final_report.xml',
    ],
    "assets": {
        'web.assets_backend': [
        'aspl_payroll_and_contract_extension/static/src/css/it_statement.css',
        'aspl_payroll_and_contract_extension/static/src/js/it_statement.js',
        ],
        'web.assets_qweb': [

        'aspl_payroll_and_contract_extension/static/src/xml/it_statement.xml',
        ],
    },
    "application": True,
    "installable": True,
    'pre_init_hook': '_pre_init_update_rule',
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
