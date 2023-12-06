# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class CrmFollowupLines(models.Model):
    _name = "crm.followup.lines"
    _description = "CrmFollowupLines"
    _order = "frequency_days"

    name = fields.Char(string="Name")
    crm_followup_template_id = fields.Many2one('crm.followup', string='Crm Followup Template')
    frequency_days = fields.Integer(string="Frequency Days")
    add_context = fields.Html(string="Add Context",
                              default='''
                        # Available variables : </br>
                           ******************* </br>
                        # {{name}} : crm.lead Client Name</br>
                        # {{company}} : crm.lead Company Name </br>
                        # {{website}} : crm.lead Website </br>
                        
                        </br></br>
                        # Note: returned value have to be set in the variable From CRM Lead.
                        ''')
