def should_revise_review(state):
    if state["revision_count"] >= state["max_revisions"]:
        return "finalize"

    if state["review_critique"].needs_revision:
        return "revise"

    return "finalize"

def should_search_more(state):
    if state["search_iterations"] >= state["max_search_iterations"]:
        return "summarize_papers"

    if state["coverage_analysis"].is_sufficient:
        return "summarize_papers"

    if not state["followup_queries"]:
        return "summarize_papers"

    return "search_more"