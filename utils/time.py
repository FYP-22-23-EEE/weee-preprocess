import datetime

def parse_simple_timedelta(delta_str):
    if delta_str[-1] == 's':
        return datetime.timedelta(seconds=int(delta_str[:-1]))
    raise ValueError('Unsupported time delta format')