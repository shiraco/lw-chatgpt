from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Memo(Base):
    __tablename__ = 'memos'

    memo_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String, index=True)


class Conversation(Base):
    __tablename__ = 'conversasions'

    id: Mapped[int] = mapped_column(primary_key=True)
    # domain_id: Mapped[str] = mapped_column(String, nullable=False)
    # bot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # channel_id: Mapped[str] = mapped_column(String, nullable=True)
    # user_id: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    # send_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
