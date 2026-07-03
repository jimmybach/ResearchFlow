from src.prompts.summarize_papers import SUMMARIZE_PAPER_PROMPT
from src.schema.summary import PaperSummary
import logging
from src.services.llm import llm
from src.graph.state import GraphState

async def summarize_papers_node(state: GraphState):
    logger=logging.getLogger(__name__)
    logger.debug(f"Summarizing {len(state['ranked_papers'])} papers for question: {state['question']}")
    
    paper_summaries = []
    chain=SUMMARIZE_PAPER_PROMPT | llm.with_structured_output(PaperSummary)
    
    for paper in state["ranked_papers"]:
        summary = await chain.ainvoke({
            "question": state["question"],
            "pmid": paper.pmid,
            "title": paper.title,
            "abstract": paper.abstract,
        })

        paper_summaries.append(summary)

    return {
        "paper_summaries": paper_summaries
    }