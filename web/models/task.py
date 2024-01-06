from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import AutoIncrementIdMixin, BaseModel


class Task(AutoIncrementIdMixin, BaseModel):
    __tablename__ = "task"

    name: Mapped[str]
    sub_tasks: Mapped[list[SubTask]] = relationship(
        back_populates="task", passive_deletes=True
    )


class SubTask(AutoIncrementIdMixin, BaseModel):
    __tablename__ = "sub_task"

    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"), index=True
    )
    task: Mapped[Task] = relationship(back_populates="sub_tasks")
