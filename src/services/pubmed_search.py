import re

from src.services.mcp.pubmed import pubmed_service
from src.utils.pubmed import extract_pmids, parse_paper


async def search_pubmed_papers(queries: list[str]) -> list[dict]:
    papers_list = []
    seen_pmids = set()

    for query in queries:
        search_result = await pubmed_service.search(query)

        pmids = extract_pmids(search_result)

        new_pmids = [
            pmid for pmid in pmids
            if pmid not in seen_pmids
        ]

        seen_pmids.update(new_pmids)

        if not new_pmids:
            continue
        
        papers = await pubmed_service.fetch_papers_cached(new_pmids)

        papers_list.extend(papers)

    return papers_list