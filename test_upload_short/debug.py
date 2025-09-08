import os, csv, sys, time, uuid, traceback
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional

from datetime import datetime, timedelta, timezone
TZ_OFFSET_HOURS = 7
def local_now() -> datetime:
    utc_now = datetime.now(timezone.utc)
    return utc_now + timedelta(hours=TZ_OFFSET_HOURS)

def ensure_file(path: str, header: List[str]):
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(header)

