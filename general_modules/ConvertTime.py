
def ms_to_24_hour_time_format(ms):
    text = ""
    if ms >= 3600000:
        hours = ms//3600000
        ms = ms%3600000
        text += f"{hours}h"
    if ms >= 60000:
        minutes = ms//60000
        ms = ms%60000
        text += f" {minutes}m"
    seconds = ms//1000
    text += f" {seconds}s"
    return text
