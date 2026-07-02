from pydantic import BaseModel

class Paper(BaseModel):
    title: str
    authors: list[str]
    journal: str
    pmid: str
    doi: str
    abstract: str