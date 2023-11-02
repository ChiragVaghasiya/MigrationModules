from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Blocked_Emails(models.Model):
    _name = "block.emails"
    _description = "Blocked Emails list for Leads"

    email = fields.Char("Email", required=True)

class Email_Blocking(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create(self,vals):
        blocked_emails =self.env['block.emails'].search([])
        tag=0
        if vals.get('email_from'):
            for i in blocked_emails:
                if i.email in vals.get('email_from'):
                    tag=1
        if tag != 1:
            result = super(Email_Blocking,self).create(vals)
            return result 
        else:
            raise ValidationError('A Glitch Was Found')
    