from src.services.llm import llm
from src.graph.state import GraphState
from schema.lit_review import LiteratureReview
from prompts.revise_lit_review import REVISE_REVIEW_PROMPT
import logging



async def revise_literature_review_node(state: GraphState):
    logger=logging.getLogger(__name__)
    logger.debug(f"Revising literature review for question: {state['question']}")
    
    chain=REVISE_REVIEW_PROMPT | llm.with_structured_output(LiteratureReview)

    literature_review = await chain.ainvoke(
        {
            "literature_review": state["literature_review"],
            "question": state["question"],
            "paper_summaries": state["paper_summaries"],
            "critique": state["review_critique"]
        }
    )

    return {"literature_review": literature_review,
            "revision_count": state["revision_count"] + 1}