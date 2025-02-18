from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func



class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class ExpenseModel(Base):
    __tablename__ = "expenses"

    name: Mapped[str]
    amount: Mapped[float]
    comment: Mapped[str] = mapped_column(nullable=True)
