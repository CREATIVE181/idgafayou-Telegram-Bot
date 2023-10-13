import datetime


async def seconds_to_unix(timedelta=None):
    return (
        datetime.datetime.now().timestamp()
        if timedelta is None
        else (datetime.datetime.now() + timedelta).timestamp()
    )


async def time_to_timedelta(time):
    numb, mhd = int(time[:-1]), time[-1]
    if mhd in ['m', 'м']:
        timedelta = datetime.timedelta(minutes=numb)
    elif mhd in ['h', 'ч']:
        timedelta = datetime.timedelta(hours=numb)
    elif mhd in ['d', 'д']:
        timedelta = datetime.timedelta(days=numb)
    return await seconds_to_unix(timedelta)