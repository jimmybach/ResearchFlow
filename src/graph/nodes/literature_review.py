from src.services.llm import llm
from src.graph.state import GraphState
from schema.lit_review import LiteratureReview
from prompts.literature_review import synthesize_literature_prompt
import logging

async def review_literature_node(state: GraphState) -> dict:
    logger=logging.getLogger(__name__)
    logger.debug(f"Summarizing {len(state['paper_summaries'])} paper summaries for question: {state['question']}")
    
    chain=synthesize_literature_prompt | llm.with_structured_output(LiteratureReview)
    review = await chain.ainvoke({"question": state["question"], "paper_summaries": state["paper_summaries"]})
    
    return {
        "literature_review": review
    }

