from contextlib import contextmanager
import logging
from datetime import date
from odoo import SUPERUSER_ID, api, http

import odoo
import werkzeug
import base64

_logger = logging.getLogger(__name__)

from odoo import _, http
from odoo.addons.mail_tracking.controllers.main import MailTrackingController


BLANK = "R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="

@contextmanager
def db_env(dbname):
    if not http.db_filter([dbname]):
        raise werkzeug.exceptions.BadRequest()
    cr = None
    if dbname == http.request.db:
        cr = http.request.cr
    if not cr:
        cr = odoo.sql_db.db_connect(dbname).cursor()
    yield api.Environment(cr, SUPERUSER_ID, {})

class MailTrackingControllerExtend(MailTrackingController):


    @http.route(
        [
            "/mail/tracking/open/<string:db>" "/<int:tracking_email_id>/blank.gif",
            "/mail/tracking/open/<string:db>"
            "/<int:tracking_email_id>/<string:token>/blank.gif",
        ],
        type="http",
        auth="none",
        methods=["GET"],
    )
    def mail_tracking_open(self, db, tracking_email_id, token=False, **kw):
        """Route used to track mail openned (With & Without Token)"""

        metadata = self._request_metadata()
        with db_env(db) as env:
            try:
                tracking_email = env["mail.tracking.email"].search(
                    [("id", "=", tracking_email_id), ("token", "=", token)]
                )
                if not tracking_email:
                    _logger.warning(
                        "MailTracking email '%s' not found", tracking_email_id
                    )
                elif tracking_email.state in ("sent", "delivered"):
                    activity_data = {
                        'activity_type_id': env.ref('mail.mail_activity_data_email').id,
                        'summary':'Opened (' + tracking_email.mail_message_id.record_name + ').',
                        'note':'Opened (' + tracking_email.mail_message_id.record_name + ').',
                        'date_deadline': date.today(),
                        'res_model_id': env['ir.model'].sudo().search([('model', '=', tracking_email.mail_message_id.model)]).id,
                        'res_id': tracking_email.mail_message_id.res_id,
                    }
                    mail_activity = env['mail.activity'].create(activity_data)
                    # mail_activity.action_done()
                    tracking_email.event_create("open", metadata)
                    
            except Exception as e:
                _logger.warning(e)

        # Always return GIF blank image
        response = werkzeug.wrappers.Response()
        response.mimetype = "image/gif"
        response.data = base64.b64decode(BLANK)
        return response
