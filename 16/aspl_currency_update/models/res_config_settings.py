# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    _name = "res.config.settings"

    api_key = fields.Char(string="API Key", related='company_id.api_key', readonly=False)
