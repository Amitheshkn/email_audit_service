import email
import email.policy
from typing import Any

from email_audit_app.core.rule_engine import RuleEngine
from email_audit_app.core.schemas.audit_schema import AuditResult


class AuditService:
    @staticmethod
    def audit(eml_path: str,
              /) -> AuditResult:
        email_content = AuditService._parse_eml(eml_path)

        return RuleEngine().evaluate(email_content)

    @staticmethod
    def _parse_eml(eml_path: str,
                   /) -> dict[str, Any]:
        if not eml_path:
            raise FileNotFoundError(f"EML file not found: {eml_path}")

        try:
            with open(eml_path, 'rb') as f:
                msg = email.message_from_bytes(f.read(), policy=email.policy.default)

            content = {
                'subject': msg.get('subject', ''),
                'from': msg.get('from', ''),
                'to': msg.get('to', ''),
                'cc': msg.get('cc', ''),
                'date': msg.get('date', ''),
                'body': '',
                'attachments': []
            }

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        content['body'] += part.get_content()
                    except Exception as e:
                        content['body'] += f"[Error reading content: {str(e)}]"

                elif content_type.startswith(('image/', 'application/', 'audio/', 'video/')):
                    attachment = {
                        'filename': part.get_filename() or '[unnamed]',
                        'type': content_type,
                        'size': len(part.get_payload(decode=True)) if part.get_payload() else 0
                    }
                    content['attachments'].append(attachment)

            return content

        except PermissionError as e:
            raise PermissionError(f"Permission denied accessing EML file: {eml_path}") from e

        except Exception as e:
            raise ValueError(f"Invalid EML file format: {str(e)}") from e
