def should_revise_review(state):
    if state["revision_count"] >= state["max_revisions"]:
        return "finalize"

    if state["review_critique"].needs_revision:
        return "revise"

    return "finalize"