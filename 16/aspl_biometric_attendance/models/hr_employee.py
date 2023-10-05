from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    biometric_no = fields.Char("Biometric Code", size=10)
