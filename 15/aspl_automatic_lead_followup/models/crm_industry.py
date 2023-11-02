from odoo import models, fields, api, _


class CrmIndustry(models.Model):
    _name = "crm.industry"
    _description = "Crm Industry"
    _rec_name = "industry_name"

    industry_name = fields.Char(string="Industry Name")
