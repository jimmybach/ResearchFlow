from langchain_core.prompts import ChatPromptTemplate

CRITIQUE_REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert academic editor specializing in biomedical
literature reviews.

Your task is to critically evaluate a literature review.

Be objective and evidence-based.
Do not rewrite the review.
Return only the requested structured output.
"""
    ),
    (
        "human",
        """
Research Question
-----------------
{question}

Paper Summaries
---------------
{paper_summaries}

Literature Review
-----------------
{literature_review}

Evaluate the review according to these criteria:

1. Does it answer the research question?
2. Are all major themes from the paper summaries represented?
3. Does it accurately reflect the evidence?
4. Are there unsupported claims or hallucinations?
5. Is it organized by themes instead of individual papers?
6. Are limitations and research gaps discussed?
7. Is anything important missing?

If the review is already high quality, set
needs_revision = false.

Otherwise:
- explain why
- provide concrete revision instructions
"""
    )
])