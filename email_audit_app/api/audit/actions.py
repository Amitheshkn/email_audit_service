from http import HTTPStatus
from typing import Optional

from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import ImmutableMultiDict

from email_audit_app.api.audit import utils
from email_audit_app.api.audit.audit_service import AuditService
from email_audit_app.core.schemas.audit_schema import AuditResult
from email_audit_app.core.schemas.audit_schema import AuditStatus


class AuditActions:
    @staticmethod
    def _file_validation(files: ImmutableMultiDict[str, FileStorage],
                         /) -> Optional[str]:
        if not files or "file" not in files:
            return "No file uploaded"

        if len(files.getlist("file")) > 1:
            return "Only one file can be uploaded at a time"

        file = files["file"]
        if not file or file.filename == "":
            return "Empty file provided"

        if not isinstance(file, FileStorage):
            return "Invalid file format"

        if not file.filename.lower().endswith('.eml'):
            return "Invalid file type. Only '.eml' file(s) are allowed"

        # Check if file is empty
        file.seek(0, 2)  # Seek to end
        if file.tell() == 0:
            return "File is empty"

        file.seek(0)  # Reset file pointer

        return None

    @staticmethod
    def audit_email(files: ImmutableMultiDict[str, FileStorage],
                    /) -> tuple[AuditResult, HTTPStatus]:
        validation = AuditActions._file_validation(files)
        if validation:
            return AuditResult(
                status=AuditStatus.FAILED,
                error=validation
            ), HTTPStatus.BAD_REQUEST

        file = files["file"]
        file_path = utils.store_files(file, "emails")
        try:
            return AuditService.audit(file_path), HTTPStatus.OK

        except Exception as e:
            return AuditResult(
                status=AuditStatus.FAILED,
                error=str(e)
            ), HTTPStatus.INTERNAL_SERVER_ERROR

        finally:
            utils.discard_files(file_path)
