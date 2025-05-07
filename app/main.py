from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="MINDSHEAR.AI",
    description="AI-Powered Smart Learning Assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Import and include routers
from app.api.v1 import notes, research, humanize, pdf_query

app.include_router(notes.router, prefix="/api/v1/notes", tags=["Smart Notes Generator"])
app.include_router(research.router, prefix="/api/v1/research", tags=["Research AI"])
app.include_router(humanize.router, prefix="/api/v1/humanize", tags=["Humanize AI"])
app.include_router(pdf_query.router, prefix="/api/v1/pdf", tags=["PDF Query Engine"])

@app.get("/")
async def root():
    return {"message": "Welcome to MINDSHEAR.AI API"} 