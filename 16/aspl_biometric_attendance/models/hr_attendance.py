# -*- coding: utf-8 -*-

from odoo import tools, models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class IrRule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    def archive_attendance_rule(self):
        if self.env.ref('hr_attendance.hr_attendance_rule_attendance_manager', raise_if_not_found=False):
            self.env.ref('hr_attendance.hr_attendance_rule_attendance_manager').update({'active': False})


class HrAttendance(models.Model):
    _inherit = ['hr.attendance']
    comment = fields.Text('Details')
    atten_status = fields.Boolean("Status")
    has_error = fields.Boolean("Mistake")
