{
    'name': "Currency Rate Update",
    'summary': "Update exchange rates from Exchangereates(APILayer)",
    'description': """
    """,
    'author': "Aspire Softserv Private Limited",
    'website': "https://aspiresoftserv.com",
    'category': 'Accounting',
    'version': '0.0.9',
    'price': 11.99,
    'currency': 'USD',
    'depends': ['base', 'account'],
    'data': [
        'data/currency_rates_updation.xml',
        'views/res_config_settings.xml',
        'views/res_currency.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
    "installable": True,
    "support": "odoo@aspiresoftserv.com",
}
