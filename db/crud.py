from sqlalchemy.orm import Session
from sqlalchemy import desc
from db import model, schema


def get_conversations(db: Session, skip: int = 0, limit: int = 8):
    return db.query(model.Conversation).offset(skip).limit(limit).all()


def get_conversations_for_chatgpt_filter_by_channel_id(channel_id: int, db: Session, skip: int = 0, limit: int = 8):
    return db.query(model.Conversation.id, model.Conversation.sender_type, model.Conversation.content, model.Conversation.channel_id, model.Conversation.user_id, model.Conversation.created_at).\
        order_by(desc(model.Conversation.id)).\
        filter(model.Conversation.content_type == "text", model.Conversation.channel_id == channel_id).\
        offset(skip).limit(limit).\
        all()


def get_conversations_for_chatgpt_filter_by_user_id(user_id: int, db: Session, skip: int = 0, limit: int = 8):
    return db.query(model.Conversation.id, model.Conversation.sender_type, model.Conversation.content, model.Conversation.channel_id, model.Conversation.user_id, model.Conversation.created_at).\
        order_by(desc(model.Conversation.id)).\
        filter(model.Conversation.content_type == "text", model.Conversation.user_id == user_id, model.Conversation.channel_id == None).\
        offset(skip).limit(limit).\
        all()


def create_conversation(db: Session, conversation: schema.ConversationCreatingSchema):
    db_conversation = model.Conversation(
        content_type=conversation.content_type,
        content=conversation.content,
        channel_id=conversation.channel_id,
        sender_type=conversation.sender_type,
        user_id=conversation.user_id,
        domain_id=conversation.domain_id,
        bot_id=conversation.bot_id,
        package_id=conversation.package_id,
        sticker_id=conversation.sticker_id,
        created_at=conversation.created_at
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation
