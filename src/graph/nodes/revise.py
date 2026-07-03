from src.services.llm import llm
from src.graph.state import GraphState
from src.schema.synthesis import LiteratureSynthesis
from src.prompts.revise import REVISE_REVIEW_PROMPT
import logging



async def revise_literature_synthesis_node(state: GraphState):
    logger=logging.getLogger(__name__)
    logger.debug(f"Revising literature synthesis for question: {state['question']}")
    
    chain=REVISE_REVIEW_PROMPT | llm.with_structured_output(LiteratureSynthesis)

    literature_synthesis = await chain.ainvoke(
        {
            "literature_synthesis": state["literature_synthesis"],
            "question": state["question"],
            "paper_summaries": state["paper_summaries"],
            "critique": state["review_critique"]
        }
    )

    return {"literature_synthesis": literature_synthesis,
            "revision_count": state["revision_count"] + 1}