from pydantic import BaseModel


class Citation(BaseModel):
    pmid: str
    title: str
    apa: str
    url: str