import logging
from src.prompts.coverage import ANALYZE_COVERAGE_PROMPT
from src.services.llm import llm
from src.schema.coverage import CoverageAnalysis


def format_papers_for_coverage(papers):
    return "\n\n".join(
        f"""
PMID: {p.pmid}
Title: {p.title}
Abstract: {(p.abstract or '')[:1000]}
"""
        for p in papers
    )


async def analyze_coverage_node(state):
    chain = ANALYZE_COVERAGE_PROMPT | llm.with_structured_output(CoverageAnalysis)

    analysis = await chain.ainvoke({
        "question": state["question"],
        "papers": format_papers_for_coverage(state["ranked_papers"]),
    })

    return {
        "coverage_analysis": analysis,
        "followup_queries": analysis.recommended_next_queries,
    }