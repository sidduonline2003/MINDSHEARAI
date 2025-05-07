from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional, List
from pydantic import BaseModel
from app.services.notes_generator import NotesGenerator
from app.core.config import settings

router = APIRouter()

class NotesRequest(BaseModel):
    topic: str
    depth: str = "intermediate"  # beginner, intermediate, advanced
    include_diagrams: bool = True
    include_tables: bool = True
    style: str = "academic"  # academic, casual, technical

class NotesResponse(BaseModel):
    pdf_url: str
    text_content: str
    images: List[str]
    tables: List[dict]

@router.post("/generate", response_model=NotesResponse)
async def generate_notes(request: NotesRequest):
    try:
        notes_generator = NotesGenerator()
        result = await notes_generator.generate(
            topic=request.topic,
            depth=request.depth,
            include_diagrams=request.include_diagrams,
            include_tables=request.include_tables,
            style=request.style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/customize")
async def customize_notes(
    pdf_file: UploadFile = File(...),
    modifications: str = Form(...)
):
    try:
        notes_generator = NotesGenerator()
        result = await notes_generator.customize(pdf_file, modifications)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 