from pydantic import BaseModel, Field

class ReviewCritique(BaseModel):
    needs_revision: bool
    overall_score: int = Field(description="Overall score of the review, on a scale from 1 to 5.")

    missing_topics: list[str]
    unsupported_claims: list[str]
    factual_errors: list[str]
    organization_feedback: str
    strengths: list[str]

    revision_instructions: list[str]