from typing import TypedDict
from src.schema.summary import LiteratureSummary
from src.schema.queries import SearchQueries
from src.schema.paper import Paper
class GraphState(TypedDict):
    question: str
    queries: SearchQueries
    papers: list[Paper]
    summary: LiteratureSummary