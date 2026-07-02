from src.graph.state import GraphState
from src.services.pubmed_search import search_pubmed_papers
import logging

async def search_pubmed_node(state: GraphState):
    logger=logging.getLogger(__name__)
    logger.debug(f"Searching PubMed for queries: {state['queries']}")
    
    papers_list= await search_pubmed_papers(state["queries"])
    
    return {
        "papers": papers_list
    }

