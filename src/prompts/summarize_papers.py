from langchain_core.prompts import ChatPromptTemplate


SUMMARIZE_PAPER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert biomedical research assistant.

Summarize the paper accurately and concisely (< 100 words).
Do not invent details that are not in the title or abstract.
Return only the structured output.
"""
    ),
    (
        "human",
        """
User research question:
{question}

Paper:
PMID: {pmid}
Title: {title}
Abstract:
{abstract}

Summarize this paper for use in a literature review.
"""
    )
])