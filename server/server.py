import os
from flask import Flask, flash, request, redirect, render_template
import gdrive
from pathlib import Path

app = Flask(__name__)

UPLOAD_DIRECTORY = "uploads"
DRIVE_FOLDER_ID = "1OU2lDhrsLSr-l2MR0-3rbYV4bzwyOtQA"

@app.route("/upload/<path:path>", methods=["put"])
def upload(path):
    local_path = Path(os.path.join(UPLOAD_DIRECTORY, path))

    # Create directory up to file
    local_path.parent.mkdir(parents=True, exist_ok=True)

    if not local_path.exists():
        with open(str(local_path), "wb") as fp:
            fp.write(request.data)

        # Write to google drive
        gdrive.uploadFile(local_path, parent=DRIVE_FOLDER_ID)

    return "", 201
