from datetime import datetime, timedelta, timezone


def utcnow() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def utcfromtimestamp(ts: float) -> datetime:
    return datetime.utcfromtimestamp(ts).replace(tzinfo=timezone.utc)


def utcnow_plus_seconds(sec: int) -> datetime:
    return utcnow() + timedelta(seconds=sec)
