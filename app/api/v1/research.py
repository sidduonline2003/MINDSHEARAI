from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from pydantic import BaseModel
from app.services.research_ai import ResearchAI

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str
    max_results: int = 5

class PaperAnalysisRequest(BaseModel):
    paper_content: str

class LiteratureReviewRequest(BaseModel):
    topic: str
    papers: List[dict]

@router.post("/search")
async def search_research(request: ResearchRequest):
    try:
        research_ai = ResearchAI()
        results = await research_ai.search_research(
            query=request.query,
            max_results=request.max_results
        )
        return {"papers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_paper(request: PaperAnalysisRequest):
    try:
        research_ai = ResearchAI()
        analysis = await research_ai.analyze_paper(request.paper_content)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/literature-review")
async def generate_literature_review(request: LiteratureReviewRequest):
    try:
        research_ai = ResearchAI()
        review = await research_ai.generate_literature_review(
            topic=request.topic,
            papers=request.papers
        )
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 