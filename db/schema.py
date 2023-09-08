from pydantic import BaseModel, Field


class ConversationSchema(BaseModel):
    id: int = Field()
    content: str = Field(max_length=200)

    class Config:
        orm_mode = True


class ConversationCreatingSchema(BaseModel):
    content: str = Field(max_length=200)

    class Config:
        orm_mode = True
