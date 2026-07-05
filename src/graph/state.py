from typing import TypedDict
from pydantic import Field
from src.schema.review_critique import ReviewCritique
from src.schema.summary import PaperSummary
from src.schema.lit_review import LiteratureReview
from src.schema.queries import SearchQueries
from src.schema.coverage import CoverageAnalysis
from src.schema.paper import Paper
from src.schema.citations import Citation
class GraphState(TypedDict):
    question: str
    queries: SearchQueries
    papers: list[Paper]
    ranked_papers: list[Paper]
    citations: list[Citation]
    paper_summaries: list[PaperSummary]
    coverage_analysis: CoverageAnalysis
    followup_queries: list[str]
    search_iterations: int = Field(default=0)
    max_search_iterations: int = Field(default=3)
    literature_review: LiteratureReview
    revision_count: int = Field(default=0)
    max_revisions: int = Field(default=2)
    review_critique: ReviewCritique
    export_paths: dict[str,str]