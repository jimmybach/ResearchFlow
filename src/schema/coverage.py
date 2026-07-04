from pydantic import BaseModel


class CoverageGap(BaseModel):
    missing_topic: str
    why_it_matters: str
    suggested_query: str


class CoverageAnalysis(BaseModel):
    is_sufficient: bool
    covered_topics: list[str]
    weak_topics: list[str]
    missing_topics: list[CoverageGap]
    recommended_next_queries: list[str]
    explanation: str