from src.services.ranking import rank_papers_by_similarity
import logging

async def rank_papers_node(state):
    logger=logging.getLogger(__name__)
    logger.debug(f"Ranking {len(state.get('papers', []))} papers for question: {state.get('question', '')}")
    papers = state.get("papers", [])
    question = state.get("question", "")
    
    ranked_papers = await rank_papers_by_similarity(papers, question, top_k=state.get('top_k', 20))
    
    return {"ranked_papers": ranked_papers}