from src.services.llm import llm
from src.graph.state import GraphState
from src.schema.summary import LiteratureSummary
from src.prompts.summarize import summarize_prompt
import logging

async def summarize_node(state: GraphState) -> dict:
    logger=logging.getLogger(__name__)
    logger.debug(f"Summarizing {len(state['papers'])} papers for question: {state['question']}")
    
    chain=summarize_prompt | llm.with_structured_output(LiteratureSummary)
    summary = await chain.ainvoke({"question": state["question"], "papers": state["papers"]})
    return {
        "summary": summary
    }

