from src.graph.state import GraphState
from src.prompts.review import CRITIQUE_REVIEW_PROMPT
from src.schema.review import ReviewCritique
from src.services.llm import llm
from src.utils.review import should_revise_review

async def review_literature_synthesis_node(state: GraphState):
    chain=CRITIQUE_REVIEW_PROMPT | llm.with_structured_output(ReviewCritique)

    review_critique = await chain.ainvoke(
        {
            "literature_synthesis": state["literature_synthesis"],
            "question": state["question"],
            "paper_summaries": state["paper_summaries"]
        }
    )

    return {"review_critique": review_critique}