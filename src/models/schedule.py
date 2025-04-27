from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config import settings
from src.db import Base
from src.utils import global_utils


class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = (
        UniqueConstraint(
            "lastname", "firstname", "patronymic", name="uq_teacher_fullname"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lastname: Mapped[str]
    firstname: Mapped[str]
    patronymic: Mapped[str]
    birthday: Mapped[date]

    @property
    def fullname(self) -> str:
        return f"{self.lastname} {self.firstname} {self.patronymic}"

    @property
    def initials(self) -> str:
        return f"{self.lastname} {self.firstname[:1]}. {self.patronymic[:1]}."

    @property
    def age(self) -> int:
        birthday_combined = datetime.combine(
            self.birthday, datetime.min.time(), tzinfo=settings.TIMEZONE
        )

        now = global_utils.get_local_now()
        delta_age = now - birthday_combined
        years = int(delta_age.days / 365.25)
        return years


class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Lecture(Base):
    __tablename__ = "lectures"

    id: Mapped[int] = mapped_column(primary_key=True)
    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), unique=True, index=True
    )
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    cabinet: Mapped[str]
    is_practice: Mapped[bool]

    discipline: Mapped[Discipline] = relationship()
    teacher: Mapped[Teacher] = relationship()
