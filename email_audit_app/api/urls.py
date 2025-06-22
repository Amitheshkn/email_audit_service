from flask import Flask
from flask_cors import CORS

from email_audit_app.api.audit.routes import audit_app

app = Flask("email_audit_app")

CORS(app)

app.register_blueprint(audit_app)
