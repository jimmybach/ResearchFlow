from src.graph.state import GraphState
from prompts.review_lit_review import CRITIQUE_REVIEW_PROMPT
from schema.review_critique import ReviewCritique
from src.services.llm import llm

async def review_literature_review_node(state: GraphState):
    chain=CRITIQUE_REVIEW_PROMPT | llm.with_structured_output(ReviewCritique)

    review_critique = await chain.ainvoke(
        {
            "literature_review": state["literature_review"],
            "question": state["question"],
            "paper_summaries": state["paper_summaries"]
        }
    )

    return {"review_critique": review_critique}