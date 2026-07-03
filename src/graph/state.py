from typing import TypedDict
from pydantic import Field
from schema.review_critique import ReviewCritique
from src.schema.summary import PaperSummary
from schema.lit_review import LiteratureReview
from src.schema.queries import SearchQueries
from src.schema.paper import Paper
class GraphState(TypedDict):
    question: str
    queries: SearchQueries
    papers: list[Paper]
    ranked_papers: list[Paper]
    paper_summaries: list[PaperSummary]
    literature_review: LiteratureReview
    revision_count: int = Field(default=0)
    max_revisions: int = Field(default=2)
    review_critique: ReviewCritique