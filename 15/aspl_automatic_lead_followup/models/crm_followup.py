# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import html
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields


class CrmFollowup(models.Model):
    _name = "crm.followup"
    _description = "Crm Followup"
    _rec_name = "name"

    name = fields.Char(string="Followup Name")
    crm_followup_line_ids = fields.One2many('crm.followup.lines', 'crm_followup_template_id', string='Crm Followup')

    def mail_sender(self, crm_obj, line_obj):
        search_words = ["{{name}}", "{{ name }}", "{name}", "{ name }", "{{company}}", "{{ company }}",
                        "{company}", "{ company }", "{{website}}", "{{ website }}", "{website}",
                        "{ website }"]
        body_content = line_obj.add_context
        for word in search_words:
            if word == "{{name}}" or word == "{{ name }}" or word == "{name}" or word == "{ name }":
                if crm_obj.contact_name:
                    body_content = body_content.replace(word, crm_obj.contact_name)
                else:
                    body_content = body_content.replace(word, '')
            elif word == "{{company}}" or word == "{{ company }}" or word == "{company}" or word == "{ company }":
                if crm_obj.partner_name:
                    body_content = body_content.replace(word, crm_obj.partner_name)
                else:
                    body_content = body_content.replace(word, '')
            elif word == "{{website}}" or word == "{{ website }}" or word == "{website}" or word == "{ website }":
                if crm_obj.website:
                    body_content = body_content.replace(word, f'<a href="{crm_obj.website}">{crm_obj.website}</a>')
                else:
                    body_content = body_content.replace(word, '')

        b_content = body_content
        employee_id = self.env['hr.employee'].search([('user_id', '=', crm_obj.user_id.id)], limit=1)
        if employee_id:
            url = self.env['ir.config_parameter'].get_param('web.base.url')
            email_image = self.env.ref('aspl_automatic_lead_followup.email_image_record').sudo().id
            location_image = self.env.ref('aspl_automatic_lead_followup.location_image_record').sudo().id
            phone_image = self.env.ref('aspl_automatic_lead_followup.phone_image_record').sudo().id
            right_arrow_image = self.env.ref('aspl_automatic_lead_followup.right_arrow_image_record').sudo().id
            website_image = self.env.ref('aspl_automatic_lead_followup.website_image_record').sudo().id

            body_content = body_content + f'</br></br><div style="margin-bottom:-24px;"><table style="border-collapse:collapse"><tbody><tr><td><table style="border-collapse:collapse"><tbody><tr><td><table style="border-collapse:collapse"><tbody><tr><td><strong style="font-weight:bolder">{employee_id.name} |&nbsp;</strong>{employee_id.job_title}</td><td><a href="https://aspiresoftserv.com/" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" style="text-decoration:none; background-color:transparent; color:#556ee6" data-linkindex="0"><img data-imagetype="External" src="https://aspiresoftserv.com/_next/static/media/aspire-logo-color.7b236c07.svg" width="0" height="0" style="border-style:none; vertical-align:middle; width:auto; height:auto"></a></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td><table style="border-collapse:collapse"><tbody><tr><td><table style="border-collapse:collapse"><tbody><tr><td><table style="border-collapse:collapse"><tbody><tr><td><p style="margin:0px; font-size:13px; font-family:&quot;Lucida Grande&quot;,Helvetica,Verdana,Arial,sans-serif"><img data-imagetype="External" src="{url}/web/image/ir.attachment/{phone_image}/datas" width="24" height="24" style="border-style:none; vertical-align:middle; width:24px; height:24px">&nbsp;{employee_id.work_phone}&nbsp;&nbsp;&nbsp;<img data-imagetype="External" src="{url}/web/image/ir.attachment/{website_image}/datas"" width="24" height="24" style="border-style:none; vertical-align:middle; width:24px; height:24px">&nbsp;<a href="{employee_id.company_id.website}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" style="text-decoration:none; background-color:transparent; color:#556ee6" data-linkindex="1">{employee_id.company_id.website}</a></p></td></tr><tr><td><p style="margin:0px; font-size:13px; font-family:&quot;Lucida Grande&quot;,Helvetica,Verdana,Arial,sans-serif"><img data-imagetype="External" src="{url}/web/image/ir.attachment/{email_image}/datas" width="24" height="24" style="border-style:none; vertical-align:middle; width:24px; height:24px">&nbsp;{employee_id.work_email}</p></td></tr><tr><td><p style="margin:0px; font-size:13px; font-family:&quot;Lucida Grande&quot;,Helvetica,Verdana,Arial,sans-serif"><img data-imagetype="External" src="{url}/web/image/ir.attachment/{location_image}/datas" width="24" height="24" style="border-style:none; vertical-align:middle; width:24px; height:24px">&nbsp;<a href="https://maps.google.com/?q={employee_id.company_id.street},&nbsp;{employee_id.company_id.street2},&nbsp;{employee_id.company_id.city},&nbsp;{employee_id.company_id.state_id.name},&nbsp;{employee_id.company_id.zip},&nbsp;{employee_id.company_id.country_id.name}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" style="text-decoration:none; background-color:transparent; color:#556ee6" data-linkindex="2">{employee_id.company_id.street}</a></p></td></tr><tr><td><p style="margin:0px; font-size:13px; font-family:&quot;Lucida Grande&quot;,Helvetica,Verdana,Arial,sans-serif"><img data-imagetype="External" src="{url}/web/image/ir.attachment/{right_arrow_image}/datas" width="24" height="24" style="border-style:none; vertical-align:middle; width:24px; height:24px">&nbsp;{employee_id.company_id.street2},&nbsp;{employee_id.company_id.city},&nbsp;{employee_id.company_id.state_id.name},&nbsp;{employee_id.company_id.zip},&nbsp;{employee_id.company_id.country_id.name}</p></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div>'

        body_content = html.unescape(body_content)
        try:
            post_params = {
                'message_type': 'comment',
                'subtype_id': 1,
                'email_layout_xmlid': 'mail.mail_notification_paynow',
                'subject': crm_obj.name,
                'body': body_content,
                'partner_ids': [crm_obj.partner_id.id],
                'author_id': self.env.user.id,
                'email_from': crm_obj.user_id.login,
                'email_to': crm_obj.partner_id.email,
            }
            ctx = dict(self.env.context)
            ctx.update({'from_lead_followup': True, 'mail_notify_force_send': True})
            message_id = crm_obj.with_context(ctx).message_post(**post_params)
        except Exception:
            message_id = False

        return [message_id, b_content]

    def followup_mail_sender(self):
        crm_lead_ids = self.env['crm.lead'].sudo().search([
            ('followup_id', '!=', False),
            ('followup_start_date', '!=', False),
            ('user_id', '!=', False),
            ('followup_replay_date', '=', False),
        ])

        for crm_obj in crm_lead_ids:
            if crm_obj.followup_start_date <= date.today():
                for line_obj in crm_obj.followup_id.crm_followup_line_ids:
                    if ((crm_obj.followup_start_date + relativedelta(days=line_obj.frequency_days)) == date.today()):
                        mail_sender = CrmFollowup.mail_sender(self, crm_obj, line_obj)
                        message_id = mail_sender[0]
                        if message_id != False:
                            crm_obj.write({
                                'last_followup_send_date': date.today(),
                            })
                            crm_obj.followup_history_line_ids.create({
                                'followup_history_id': crm_obj.id,
                                'message_id': message_id.message_id,
                                'send_on': datetime.now(),
                                'email_from': crm_obj.user_id.login,
                                'email_to': crm_obj.partner_id.email,
                                'content': mail_sender[1],
                            })
                            break
