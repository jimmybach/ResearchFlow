from pydantic import BaseModel

class Theme(BaseModel):
    title: str
    discussion: str
    supporting_pmids: list[str]

class LiteratureReview(BaseModel):
    introduction: str
    major_themes: list[Theme]
    limitations: str
    research_gaps: str
    conclusion: str
