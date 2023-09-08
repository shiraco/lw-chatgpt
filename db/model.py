from sqlalchemy import Integer, String, DateTime
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Conversation(Base):
    __tablename__ = 'conversasions'

    id: Mapped[int] = mapped_column(primary_key=True)
    domain_id: Mapped[int] = mapped_column(Integer, nullable=False)
    bot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    channel_id: Mapped[str] = mapped_column(String, nullable=True, default=None)
    sender_type: Mapped[str] = mapped_column(String, nullable=False)
    sender_id: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    package_id: Mapped[str] = mapped_column(String, nullable=True, default=None)
    sticker_id: Mapped[str] = mapped_column(String, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False)
