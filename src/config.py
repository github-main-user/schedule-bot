import math
from datetime import date, datetime, time
from parser import Lecture

import pytz

MSK_TZ = pytz.timezone('Etc/GMT-3')
SCHEDULE_UPDATE_TIME = time(22, 23, tzinfo=MSK_TZ)


def format_next_lecture(lecture: Lecture, date: date) -> str:
    minutes_left = (
        math.ceil(
            (datetime.combine(date, lecture.time) - datetime.now()).total_seconds() / 60
        ),
    )
    is_practice = 'практика' if lecture.discipline.is_practice else 'лекция'

    return (
        f'{minutes_left} minutes left before the next lecture:'
        f'*{lecture.time.strftime('%H:%M')}*: {lecture.discipline.name} ({lecture.cabinet})'
        f'{lecture.teacher} ({is_practice})'
    )


def format_lectures(lectures: list[Lecture], date: date) -> str:
    formatted_lectures = [date.strftime('*%d %b (%a)*')]
    for lecture in sorted(lectures, key=lambda l: l.time):
        formatted_lectures.append(
            f'*{lecture.time.strftime('%H:%M')}*: {lecture.discipline.name} ({lecture.cabinet})'
        )

    return '\n'.join(formatted_lectures)


def format_jobs(jobs) -> str:
    formatted_jobs = ['Scheduled jobs:\n']
    for job in jobs:
        formatted_jobs.append(
            f'Job "{job.name}":\n'
            f' - id: {job.id}\n'
            f' - callback: {job.callback}\n'
            f' - trigger: {job.trigger}\n'
        )

    return '\n'.join(formatted_jobs)
