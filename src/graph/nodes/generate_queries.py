from src.graph.state import GraphState
from src.services.llm import llm
from src.schema.queries import SearchQueries
from src.prompts.generate_queries import generate_queries_prompt
import logging

async def generate_queries_node(state: GraphState):
    logger=logging.getLogger(__name__)
    logger.debug(f"Generating queries for question: {state['question']}")

    chain= generate_queries_prompt | llm.with_structured_output(SearchQueries)
    response = await chain.ainvoke(
        {
            "question": state["question"]
        }
    )

    return {
        "queries": response.queries
    }

