from datetime import datetime, timezone


def get_current_utc_time() -> datetime:
    utc_time = datetime.now(timezone.utc)
    # return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    return utc_time
