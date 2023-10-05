# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    api_key = fields.Char(string="API Key")
