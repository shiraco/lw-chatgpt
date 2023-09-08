from sqlalchemy.orm import Session
from db import model, schema


def get_conversations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Conversation).offset(skip).limit(limit).all()


def create_conversation(db: Session, conversation: schema.ConversationCreatingSchema):
    db_conversation = model.Conversation(
        content_type=conversation.content_type,
        content=conversation.content,
        channel_id=conversation.channel_id,
        sender_type=conversation.sender_type,
        user_id=conversation.user_id,
        domain_id=conversation.domain_id,
        bot_id=conversation.bot_id,
        created_at=conversation.created_at
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
