import os
from dataclasses import dataclass
from datetime import date, datetime, time

import requests
from dotenv import load_dotenv

load_dotenv()
SCHEDULE_URL = os.getenv('SCHEDULE_URL', '')


@dataclass
class Discipline:
    name: str
    is_practice: bool


@dataclass
class Lecture:
    discipline: Discipline
    teacher: str
    cabinet: str
    time: time


class ScheduleFormer:
    def __init__(self) -> None:
        self._days = dict()
        self._schedule_time = (
            time(9, 00),
            time(10, 40),
            time(12, 40),
            time(14, 20),
            time(16, 00),
            time(17, 40),
            time(19, 20),
        )

    def _request_raw_schedule(self) -> list:
        r = requests.get(url=SCHEDULE_URL, timeout=5)
        if r.status_code != 200:
            # TODO: raise error
            print('There is some error: status code is not 200')
            exit()

        return r.json().get('scheduleChanges', [])

    def form_schedule(self) -> dict[date, list[Lecture]]:
        raw_lectures = self._request_raw_schedule()

        for lecture in raw_lectures:
            lesson_dt = datetime.combine(
                date=datetime.fromisoformat(lecture['date']).date(),
                time=self._schedule_time[lecture['lessonId'] - 1],
            )

            if lesson_dt >= datetime.now():
                self._days.setdefault(lesson_dt.date(), [])

                discipline = Discipline(
                    name=lecture['discipline']['name'],
                    is_practice=lecture['eventType']['name'] != 'Лекция',
                )

                sCabinet = lecture['svedenCabinet']
                cabinet = sCabinet['cabinet'] or sCabinet['nameForSchedule']

                l = Lecture(
                    discipline=discipline,
                    teacher=' '.join(
                        [
                            lecture['person']['lastName'],
                            lecture['person']['name'],
                            lecture['person']['secondName'],
                        ]
                    ),
                    cabinet=cabinet,
                    time=lesson_dt.time(),
                )

                self._days[lesson_dt.date()].append(l)

        return self._days
