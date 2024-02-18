import os

class DJISSU():
    BASE = os.getenv("DJISSU_BASE_DIR")
    LOGGING = f"{BASE}/logging_files"
    PY = f"{BASE}/py_files"
    JSON = f"{BASE}/json_files"

class ISSUBOT():
    BASE = os.getenv("ISSUBOT_BASE_DIR")
    LOGGING = f"{BASE}/logging_files"
    PY = f"{BASE}/py_files"
    JSON = f"{BASE}/json_files"