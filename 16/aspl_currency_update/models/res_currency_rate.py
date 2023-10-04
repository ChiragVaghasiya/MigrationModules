from odoo import models, fields, api, _


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    
    current_company_currency = fields.Many2one('res.currency', string="Base Currency")
