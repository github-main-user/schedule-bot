HELP = """\
It is a bot for the SKSI institute.
Bot fetches and shows schedule for the "ИТБ-24" group.
Bot will update schedule every day at {update_time}, and notify you about every lecture at {minutes_before} minutes before it starts.

Available commands:
- /help - show this message
- /start - start bot
- /stop - stop bot
- /next - get the nearest lecture
"""

SUBSCRIBED = "You are subscribed to receive info about upcoming lectures every day at {update_time}"
UNSUBSCRIBED = "You are unsubscribed now"
ALREADY_SUBSCRIBED = "You are already subscribed"
NOT_SUBSCRIBED = "You are not subscribed"

EMPTY_TOMORROW = "There are no lectures tomorrow"
TOMORROW_N_LECTURES = "Tomorrow will be {n} lecture(s)"

LECTURE_VERBOSE_TEMPLATE = """\
*{date}*
*{time}* {name} ({cabinet}) ({is_practice})
{teacher} ({age} yeard old)
"""
