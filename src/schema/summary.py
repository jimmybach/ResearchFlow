from pydantic import BaseModel, Field

class PaperSummary(BaseModel):
    pmid: str
    title: str
    research_question: str
    methods: str
    key_findings: list[str]
    limitations: list[str]
    relevance_to_user_question: str
