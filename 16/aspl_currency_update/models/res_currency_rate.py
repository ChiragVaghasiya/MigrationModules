# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    
    current_company_currency = fields.Many2one('res.currency', string="Base Currency")
