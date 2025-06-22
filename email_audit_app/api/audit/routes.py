from flask import Blueprint
from flask import request

from email_audit_app.api.audit.actions import AuditActions

audit_app = Blueprint('audit', __name__)


@audit_app.route("/email/audit", methods=["POST"])
def audit_email():
    files = request.files

    try:
        result, status_code = AuditActions.audit_email(files)

        return result.model_dump(exclude_none=True), status_code

    except Exception as e:
        return {"error": str(e)}, 500
