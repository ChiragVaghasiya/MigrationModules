# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import requests
from odoo import models, fields, api, _
import json
from datetime import datetime, date


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def cron_currency_update(self):
        company_id = self.env.company
        company_name_confirmation = self.env['res.config.settings'].search([('company_id', '=', company_id.id)])
        currency_id = company_name_confirmation.currency_id

        config_setting_obj = self.env['res.config.settings'].search([], limit=1, order='create_date desc')
        headers = {
            "apikey": config_setting_obj.api_key
        }
        payload = {}
        active_currency = ""
        for active_cur in self.env['res.currency'].search([('active', '=', True)]):
            active_currency += active_cur.name + ","
        url = "http://api.exchangeratesapi.io/v1/latest?access_key=" + config_setting_obj.api_key + "&symbols=" + active_currency[:-1]
        http_response = requests.request("GET", url, headers=headers, data=payload)
        result = http_response.text
        rates_dict = json.loads(result)
        new_rates = rates_dict.get('rates')

        for keys, values in new_rates.items():
            new_currency_rate = self.env['res.currency'].search([('name', 'ilike', keys)])
            if new_currency_rate != company_id.currency_id:
                update_currency_rate = self.env['res.currency.rate'].search(
                    [('name', 'ilike', date.today()), ('currency_id', '=', new_currency_rate.id)])

                if int(datetime.now().strftime("%w")) not in (0, 6):
                    if not update_currency_rate:
                        company_currency = company_id.currency_id.name
                        converted_rate = values / new_rates.get(company_currency)
                        self.env['res.currency.rate'].create({
                            'company_rate': converted_rate,
                            'currency_id': new_currency_rate.id,
                            'company_id': company_id.id,
                            'current_company_currency': currency_id.id
                        })
                    else:
                        company_currency = company_id.currency_id.name
                        converted_rate = values / new_rates.get(company_currency)
                        update_currency_rate.write({'company_rate': converted_rate})
                        update_currency_rate.write({'company_id': company_id.id})
