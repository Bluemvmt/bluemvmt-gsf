from datetime import datetime

from gsfpy3_09.timespec import c_timespec


def timespec_to_datetime(original: c_timespec) -> datetime:
    epoch_time: float = float(original.tv_sec) + float(original.tv_nsec) / 1e9
    return datetime.fromtimestamp(epoch_time)
