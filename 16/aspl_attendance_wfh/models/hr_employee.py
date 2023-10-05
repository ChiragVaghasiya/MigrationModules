from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    permanent_work_from_home = fields.Boolean("Permanent Work From Home")
