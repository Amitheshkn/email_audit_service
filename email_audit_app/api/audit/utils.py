import os
import uuid

from werkzeug.datastructures import FileStorage

from email_audit_app.core.config import CONF


def store_files(file: FileStorage,
                sub_folder: str,
                /) -> str:
    if not file:
        raise ValueError("No file provided for saving.")

    filename = uuid.uuid4().hex
    save_path = os.path.join(CONF.application.file_path, sub_folder, filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    file.save(save_path)

    return save_path


def discard_files(file_path: str,
                  /) -> bool:
    if os.path.exists(file_path):
        os.remove(file_path)

    return True
