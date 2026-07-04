from src.services.pubmed_search import search_pubmed_papers

async def search_followup_pubmed_node(state):
    new_papers = await search_pubmed_papers(
        state["followup_queries"]
    )

    all_papers = state["papers"] + new_papers

    unique = {
        paper.pmid: paper
        for paper in all_papers
        if paper.pmid
    }

    return {
        "papers": list(unique.values()),
        "search_iterations": state["search_iterations"] + 1,
    }