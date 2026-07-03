# src/prompts/revise_review.py

from langchain_core.prompts import ChatPromptTemplate


REVISE_REVIEW_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert academic editor for biomedical literature reviews.

Revise the literature review using the critique.
Do not invent evidence.
Only use information supported by the paper summaries.
Return only the revised literature review.
""",
        ),
        (
            "human",
            """
Research question:
{question}

Paper summaries:
{paper_summaries}

Current literature review:
{literature_synthesis}

Critique:
{critique}

Revise the literature review.
""",
        ),
    ]
)