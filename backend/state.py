from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo

import timeouts_store
from dotenv import load_dotenv

load_dotenv()

online_members = set()
last_spin = None
history = []


def _load_persistent():
    global history, last_spin
    try:
        history = timeouts_store.load_history()
        if history:
            # set last_spin from last entry if present
            try:
                last_entry = history[-1]
                last_spin = datetime.fromisoformat(last_entry.get("time"))
            except Exception:
                last_spin = None
    except Exception:
        history = []
        last_spin = None


_load_persistent()


def is_happy_hour():
    """Check if it is currently Happy Hour (Paris time).

    By default, Happy Hour is from 17:00 to 18:00 Paris time, but can be
    customized via environment variables START_HOUR_HAPPY_HOUR and
    END_HOUR_HAPPY_HOUR (24-hour format)."""
    try:
        now = datetime.now(ZoneInfo("Europe/Paris"))
        start_hour = int(os.getenv("START_HOUR_HAPPY_HOUR", 17))
        end_hour = int(os.getenv("END_HOUR_HAPPY_HOUR", 18))
        return start_hour <= now.hour < end_hour
    except Exception:
        return False


def can_spin():
    global last_spin
    if not last_spin:
        return True

    limit = timedelta(minutes=5) if is_happy_hour() else timedelta(hours=1)
    return datetime.utcnow() - last_spin >= limit


def register_spin(member_name, member_id=None, minutes=2):
    """Register a spin in memory and persistent store.

    member_id is optional (string). If provided, it's stored alongside the
    historical display name to allow resolving the latest name later while
    preserving the original recorded name.
    """
    global last_spin
    last_spin = datetime.utcnow()
    ends_at = last_spin + timedelta(minutes=minutes)
    entry = {
        "member": member_name,
        "time": last_spin.isoformat(),
        "ends_at": ends_at.isoformat()
    }
    if member_id is not None:
        entry["member_id"] = str(member_id)
    history.append(entry)
    try:
        timeouts_store.append_entry(entry)
    except Exception:
        # best-effort: ignore persistence errors
        pass
