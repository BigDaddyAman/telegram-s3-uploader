import os
import re
import time

def sanitize_filename(name: str | None, fallback_ext: str = "") -> str:
    if not name:
        ts = time.strftime("%Y%m%d_%H%M%S")
        return f"file_{ts}{fallback_ext}"

    name = os.path.basename(name)
    name = re.sub(r"[^\w\-. ]", "_", name)
    return name.strip()
