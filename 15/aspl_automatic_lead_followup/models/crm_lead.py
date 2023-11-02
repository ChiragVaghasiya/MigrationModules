# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class CrmLead(models.Model):
    _inherit = "crm.lead"
    _order = "write_date desc"

    followup_id = fields.Many2one('crm.followup', string="Followup")
    followup_start_date = fields.Date(string="Followup Start Date")
    last_followup_send_date = fields.Date(string="Last Followup Send Date")
    followup_replay_date = fields.Date(string="Followup Replay Date")
    followup_history_line_ids = fields.One2many('followup.history', 'followup_history_id', string='Follow Up History')


class FollowupHistory(models.Model):
    _name = "followup.history"
    _description = "FollowupHistory"
    _order = "send_on desc"

    followup_history_id = fields.Many2one('crm.lead', string='Followup History')
    message_id = fields.Char(string="Message Id")
    send_on = fields.Datetime(string="Send On")
    email_from = fields.Char(string="Email From")
    email_to = fields.Char(string="Email to")
    replay_date = fields.Date(string="Replay Date")
    content = fields.Html(string="Content")
