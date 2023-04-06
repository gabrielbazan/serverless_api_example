from datetime import datetime, timezone


def get_current_utc_time() -> str:
    utc_time = datetime.now(timezone.utc)
    return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f")
