from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class SummaryBase(BaseModel):
    tech_stack: str
    learnings: str
    one_liner: str

class KnowledgeBase(BaseModel):
    title: str
    level: int
    tags: List[str]
    summary: SummaryBase
    content: str

class KnowledgeCreate(KnowledgeBase):
    pass

class Knowledge(KnowledgeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class SearchQuery(BaseModel):
    query: str

class SearchResult(BaseModel):
    knowledge: Knowledge
    relevance_score: float
    ai_summary: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
