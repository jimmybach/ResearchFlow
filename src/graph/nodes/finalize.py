async def finalize_review_node(state):
    return {
        "final_review": state["literature_synthesis"]
    }