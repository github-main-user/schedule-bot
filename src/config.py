from datetime import time

import pytz
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    TELEGRAM_TOKEN: str
    GROUP_ID: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SCHEDULE_URL(self) -> str:
        return f"https://sksi.ru/Students/ScheduleJson/?id={self.GROUP_ID}"

    TZ: pytz.BaseTzInfo = pytz.timezone("Etc/GMT-3")
    SCHEDULE_UPDATE_TIME: time = time(hour=22, minute=0, tzinfo=TZ)

    SCHEDULE_TIMES: tuple = (
        time(9, 00),
        time(10, 40),
        time(12, 40),
        time(14, 20),
        time(16, 00),
        time(17, 40),
        time(19, 20),
    )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore

#
# def format_next_lecture(lecture: Lecture, date: date) -> str:
#     minutes_left = math.ceil(
#         (datetime.combine(date, lecture.time, tzinfo=MSK_TZ) - datetime.now(tz=MSK_TZ)).total_seconds() / 60
#     )
#     is_practice = "практика" if lecture.discipline.is_practice else "лекция"
#
#     return (
#         f"{minutes_left} minutes left before the next lecture:\n"
#         f"*{lecture.time.strftime('%H:%M')}*: {lecture.discipline.name} ({lecture.cabinet})\n"
#         f"{lecture.teacher} ({is_practice})"
#     )
#
#
# def format_lectures(lectures: list[Lecture], date: date) -> str:
#     formatted_lectures = [date.strftime("*%d %b (%a)*")]
#     for lecture in sorted(lectures, key=lambda l: l.time):
#         formatted_lectures.append(f"*{lecture.time.strftime('%H:%M')}*: {lecture.discipline.name} ({lecture.cabinet})")
#
#     return "\n".join(formatted_lectures)
#
#
# def format_jobs(jobs) -> str:
#     formatted_jobs = ["Scheduled jobs:\n"]
#     for job in jobs:
#         formatted_jobs.append(
#             f'Job "{job.name}":\n' f" - id: {job.id}\n" f" - callback: {job.callback}\n" f" - trigger: {job.trigger}\n"
#         )
#
#     return "\n".join(formatted_jobs)
