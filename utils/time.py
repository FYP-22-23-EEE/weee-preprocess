import datetime

def parse_simple_timedelta(delta_str):
    if delta_str[-1] == 'ms':
        return datetime.timedelta(milliseconds=int(delta_str[:-2]))
    if delta_str[-1] == 's':
        return datetime.timedelta(seconds=int(delta_str[:-1]))
    if delta_str[-1] == 'm':
        return datetime.timedelta(minutes=int(delta_str[:-1]))
    if delta_str[-1] == 'h':
        return datetime.timedelta(hours=int(delta_str[:-1]))
    if delta_str[-1] == 'd':
        return datetime.timedelta(days=int(delta_str[:-1]))
    raise ValueError('Unsupported time delta format')