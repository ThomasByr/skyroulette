from datetime import datetime, timedelta
import os
from zoneinfo import ZoneInfo

import timeouts_store


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
    """Check if it is currently Happy Hour (17:00 - 18:00 Paris time)."""
    try:
        now = datetime.now(ZoneInfo("Europe/Paris"))
        return 17 <= now.hour < 18
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
