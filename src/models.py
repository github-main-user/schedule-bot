from datetime import date, datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    lastname: Mapped[str]
    firstname: Mapped[str]
    patronymic: Mapped[str]
    birthday: Mapped[date]

    __table_args__ = (UniqueConstraint("lastname", "fistname", "patronymic"),)


class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Lecture(Base):
    __tablename__ = "lectures"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime] = mapped_column(unique=True)
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    cabinet: Mapped[str]
    is_practice: Mapped[bool]

    discipline: Mapped[Discipline] = relationship()
    teacher: Mapped[Teacher] = relationship()
