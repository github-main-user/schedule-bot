import pytz
from datetime import time

MSK_TZ = pytz.timezone('Etc/GMT-3')
SCHEDULE_UPDATE_TIME = time(21, 0, tzinfo=MSK_TZ)

DAILY_TEMPLATE = """\
{minutes_left} minutes left before the next lecture:'
*{lecture_time}*: {lecture_name} ({cabinet})'
{teacher} ({is_practice})"""
