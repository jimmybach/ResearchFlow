from src.services.llm import llm
from src.graph.state import GraphState
from src.schema.synthesis import LiteratureSynthesis
from src.prompts.synthesize_literature import synthesize_literature_prompt
import logging

async def synthesize_literature_node(state: GraphState) -> dict:
    logger=logging.getLogger(__name__)
    logger.debug(f"Summarizing {len(state['paper_summaries'])} paper summaries for question: {state['question']}")
    
    chain=synthesize_literature_prompt | llm.with_structured_output(LiteratureSynthesis)
    synthesis = await chain.ainvoke({"question": state["question"], "paper_summaries": state["paper_summaries"]})
    
    return {
        "literature_synthesis": synthesis
    }

