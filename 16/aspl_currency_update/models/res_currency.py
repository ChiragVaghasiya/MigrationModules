import requests
from odoo import models, fields, api, _
import json
import logging
from datetime import datetime, date

_logger = logging.getLogger(__name__)


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def cron_currency_update(self):
        currency_type = self.env['res.company'].search([], limit=1, order='create_date desc')
        currency = currency_type.currency_id.name
        _logger.info("API Key:%s.............Currency:%s", currency_type.api_key, currency)
        company_id = self.env.company.id
        company_name_confirmation = self.env['res.config.settings'].search([('company_id', '=', company_id)])
        currency = company_name_confirmation.currency_id.name
        current_currency_id = company_name_confirmation.currency_id
        url = "https://api.apilayer.com/exchangerates_data/latest?base=" + currency + "&symbols="
        payload = {}
        apikey_generation = self.env['res.config.settings'].search([], limit=1, order='create_date desc')
        headers = {
            "apikey": apikey_generation.api_key
        }
        _logger.info('Header : %s', headers)
        url = "https://api.apilayer.com/exchangerates_data/latest?base=" + currency + "&symbols="
        url = "https://api.exchangeratesapi.io/v1/latest?access_key=" + apikey_generation.api_key
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        result = response.text
        rates_dict = json.loads(result)
        new_rates = rates_dict.get('rates')


        now = datetime.now()
        fmt = int(now.strftime("%w"))

        for keys, values in new_rates.items():
            new_currency_rate = self.env['res.currency'].search([('name', 'ilike', keys)])
            if new_currency_rate:
                update_currency_rate = self.env['res.currency.rate'].search(
                    [('name', 'ilike', date.today()), ('currency_id', '=', new_currency_rate.id)])

                if fmt not in (0, 6):
                    if not update_currency_rate:

                        self.env['res.currency.rate'].create({
                            'company_rate': values,
                            'currency_id': new_currency_rate.id,
                            'company_id': company_id,
                            'current_company_currency': current_currency_id.id
                        })
                    else:
                        update_currency_rate.write({'company_rate': values})
                        update_currency_rate.write({'company_id': company_id})








