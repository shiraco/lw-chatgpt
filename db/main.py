import model
import schema
import crud
from database import SessionLocal, engine

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from typing import List


model.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/conversations", response_model=List[schema.ConversationSchema])
async def read_conversations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversations = crud.get_conversations(db, skip=skip, limit=limit)
    return conversations


@app.post("/conversations", response_model=schema.ConversationSchema)
async def create_conversations(conversation: schema.ConversationCreatingSchema, db: Session = Depends(get_db)):
    return crud.create_conversation(db=db, conversation=conversation)
