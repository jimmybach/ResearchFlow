from pydantic import BaseModel, Field

class LiteratureSynthesis(BaseModel):
    overview: str = Field(description="Brief synthesis of the overall evidence.")
    consensus: list[str] = Field(description="Findings that appear consistently across papers.")
    conflicting_evidence: list[str] = Field(description="Findings that conflict or are uncertain.")
    research_gaps: list[str] = Field(description="Important gaps in the retrieved literature.")
    recommended_next_steps: list[str] = Field(description="Suggested next searches or review actions.")
    confidence: str = Field(description="High, Moderate, or Low confidence in the synthesis.")
