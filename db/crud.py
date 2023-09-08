from sqlalchemy.orm import Session
from db import model, schema


def get_conversations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Conversation).offset(skip).limit(limit).all()


def create_conversation(db: Session, conversation: schema.ConversationCreatingSchema):
    db_conversation = model.Conversation(content=conversation.content)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
