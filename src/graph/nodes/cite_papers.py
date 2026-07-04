from src.services.mcp.pubmed import pubmed_service
import logging

async def cite_papers_node(state):
    logger=logging.getLogger(__name__)
    logger.debug(f"Citing {len(state.get('ranked_papers', []))} papers.")

    pmids = [paper.pmid for paper in state["ranked_papers"]]
    citations = await pubmed_service.format_citations(pmids)
    
    return {
        "citations": citations
    }
