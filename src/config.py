from datetime import time
from zoneinfo import ZoneInfo

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

    TIMEZONE: ZoneInfo = ZoneInfo("Europe/Moscow")
    SCHEDULE_UPDATE_TIME: time = time(hour=22, minute=0, tzinfo=TIMEZONE)

    SCHEDULE_TIMES: tuple[time, ...] = (
        time(9, 00, tzinfo=TIMEZONE),
        time(10, 40, tzinfo=TIMEZONE),
        time(12, 40, tzinfo=TIMEZONE),
        time(14, 20, tzinfo=TIMEZONE),
        time(16, 00, tzinfo=TIMEZONE),
        time(17, 40, tzinfo=TIMEZONE),
        time(19, 20, tzinfo=TIMEZONE),
    )

    MINUTES_BEFORE_LECTURE: int = 15

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
