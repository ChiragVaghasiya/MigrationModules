from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _name = "res.config.settings"

    api_key = fields.Char(string="API Key", related='company_id.api_key', readonly=False)
