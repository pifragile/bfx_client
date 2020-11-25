def ms_to_age(ms):
    ms = int(ms)
    seconds = (ms // 1000) % 60
    minutes = (ms // (1000 * 60)) % 60
    hours = (ms // (1000 * 60 * 60)) % 24
    days = (ms // (1000 * 60 * 60 * 24))

    return days, hours, minutes, seconds


def ms_to_age_string(ms):
    days, hours, minutes, seconds = ms_to_age(ms)
    result = ''
    if days:
        result += f'{days} days, '
    if hours:
        result += f'{hours} hours, '
    if minutes:
        result += f'{minutes} minutes, '
    if seconds:
        result += f'{seconds} seconds'
    if result[-2:] == ', ':
        result = result[:-2]
    return result
