from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    api_key = fields.Char(string="API Key", required=True)