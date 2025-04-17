from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Note
from database import SessionLocal
from auth import get_current_user
from datetime import datetime, timezone

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class NoteRequest(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=5)

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_notes(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    notes = db.query(Note).filter(Note.user_id == user.get("id")).all()
    return notes

@router.get("/{id}/", status_code=status.HTTP_200_OK)
async def read_note(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    note_model = db.query(Note).filter(Note.id == id, Note.user_id == user.get("id")).first()
    if note_model is None:
        raise HTTPException(status_code=404, detail="Note not found.")
    return note_model

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_note(user: user_dependency, db: db_dependency, note_request: NoteRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    note_model = Note(
        title=note_request.title,
        content=note_request.content,
        user_id=user.get("id")
    )
    db.add(note_model)
    db.commit()
    db.refresh(note_model)
    return {
        "message": "Note created successfully",
        "note_id": note_model.id
    }

@router.put("/{id}/", status_code=status.HTTP_200_OK)
async def update_note(user: user_dependency, db: db_dependency, note_request: NoteRequest,
                      id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    note_model = db.query(Note).filter(Note.id == id, Note.user_id == user.get("id")).first()
    if note_model is None:
        raise HTTPException(status_code=404, detail="Note not found.")
    note_model.title = note_request.title
    note_model.content = note_request.content
    note_model.updated_at = datetime.now(timezone.utc)
    db.add(note_model)
    db.commit()
    return {
        "message": "Note updated successfully",
        "note_id": note_model.id,
        "updated_at": note_model.updated_at
    }

@router.delete("/{id}/", status_code=status.HTTP_200_OK)
async def delete_note(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    note_model = db.query(Note).filter(Note.id == id, Note.user_id == user.get("id")).first()
    if note_model is None:
        raise HTTPException(status_code=404, detail="Note not found.")
    db.delete(note_model)
    db.commit()
    return {"message": "Note deleted successfully", "note_id": id}
