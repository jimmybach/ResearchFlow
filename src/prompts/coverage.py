from langchain_core.prompts import ChatPromptTemplate


ANALYZE_COVERAGE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a biomedical research strategist.

Evaluate whether the retrieved papers provide enough coverage
to answer the research question.

Do not summarize the papers.
Identify missing or weakly covered areas.
Return only structured output.
"""
    ),
    (
        "human",
        """
Research question:
{question}

Retrieved papers:
{papers}

Assess whether the evidence base is sufficient.

Look for:
- missing subtopics
- overrepresented themes
- lack of recent evidence
- lack of methods diversity
- lack of clinical/translational evidence
- lack of mechanism-focused evidence
- lack of review/meta-analysis evidence

If coverage is insufficient, suggest targeted PubMed queries.
"""
    )
])