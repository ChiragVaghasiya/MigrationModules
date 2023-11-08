# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


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
