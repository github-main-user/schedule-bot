HELP = """\
This bot is for the SKSI institute.
It fetches and displays the schedule for the "ИТБ-24" group.
The schedule is updated daily at {update_time:%H:%M}, and you will be notified {minutes_before} minutes before each lecture begins.

Available commands:
- /help - show this message
- /start - start the bot
- /stop - stop the bot
- /next - get the next lecture"""

SUBSCRIBED = "You are now subscribed to daily updates at {update_time:%H:%M} for upcoming lectures"
UNSUBSCRIBED = "You have unsubscribed from updates"
ALREADY_SUBSCRIBED = "You are already subscribed"
NOT_SUBSCRIBED = "You are not subscribed"

EMPTY_TOMORROW = "There are no lectures tomorrow"
TOMORROW_N_LECTURES = "There will be {n} lecture(s) tomorrow"

NO_NEXT_LECTURE = "There is no next lecture"

DATE_TEMPLATE = "*{date:%d %b (%a)}*"
LECTURE_BASE_TEMPLATE = "*{time:%H:%M}*: {discipline_name} ({event_type}) ({cabinet})"
LECTURE_VERBOSE_TEMPLATE = LECTURE_BASE_TEMPLATE + "\n{teacher} ({age} years old)"
