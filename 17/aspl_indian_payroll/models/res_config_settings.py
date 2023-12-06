# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    send_payslip_by_email = fields.Boolean(string="Automatic Send Payslip By Mail", default=True)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        send_payslip_by_email = params.get_param('send_payslip_by_email', default=True)
        res.update(
            send_payslip_by_email=send_payslip_by_email
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("send_payslip_by_email",
                                                         self.send_payslip_by_email)
