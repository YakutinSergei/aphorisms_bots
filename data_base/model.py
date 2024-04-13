import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, ForeignKey, BigInteger
from data_base.database import Base

# Объявляем классы таблиц
class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    admin_check: Mapped[bool] = mapped_column(default=False)


'''Таблица афоризмов'''
class AphorismsORM(Base):
    __tablename__ = 'aphorisms'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    autor: Mapped[str]