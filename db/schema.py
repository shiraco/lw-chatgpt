from pydantic import BaseModel, Field
from datetime import datetime


class ConversationSchema(BaseModel):
    id: int = Field()
    content_type: str = Field(max_length=200)
    content: str = Field(max_length=200)
    channel_id: str = Field(max_length=200, nullable=True, default=None)
    sender_type: str = Field(max_length=200)
    sender_id: str = Field(max_length=200)
    domain_id: int = Field()
    bot_id: int = Field()
    package_id: str = Field(max_length=200, nullable=True, default=None)
    sticker_id: str = Field(max_length=200, nullable=True, default=None)
    created_at: datetime = Field()

    class Config:
        orm_mode = True


class ConversationCreatingSchema(BaseModel):
    content_type: str = Field(max_length=200)
    content: str = Field(max_length=200)
    channel_id: str = Field(max_length=200, nullable=True, default=None)
    sender_type: str = Field(max_length=200)
    sender_id: str = Field(max_length=200)
    domain_id: int = Field()
    bot_id: int = Field()
    package_id: str = Field(max_length=200, nullable=True, default=None)
    sticker_id: str = Field(max_length=200, nullable=True, default=None)
    created_at: datetime = Field(default=datetime.now())

    class Config:
        orm_mode = True
