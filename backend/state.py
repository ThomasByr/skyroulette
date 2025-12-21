from datetime import datetime, timedelta

online_members = set()
last_spin = None
history = []


def can_spin():
    global last_spin
    if not last_spin:
        return True
    return datetime.utcnow() - last_spin >= timedelta(hours=1)


def register_spin(member_name, minutes=2):
    global last_spin
    last_spin = datetime.utcnow()
    ends_at = last_spin + timedelta(minutes=minutes)
    history.append({
        "member": member_name,
        "time": last_spin.isoformat(),
        "ends_at": ends_at.isoformat()
    })
