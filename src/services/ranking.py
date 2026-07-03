from src.schema.paper import Paper
from sklearn.metrics.pairwise import cosine_similarity
from src.services.embedding import embedding_model

import numpy as np

def paper_to_text(paper: Paper) -> str:
    return f"Title: {paper.title}\n\n Abstract: {paper.abstract[:1000]}"

def prefilter_papers(paper: list[Paper]) -> list[Paper]:
    return [p for p in paper if len(paper_to_text(p)) > 100]



async def rank_papers_by_similarity(papers: list[Paper], query_text: str, top_k: int = 10) -> list[tuple[Paper, float]]:
    papers = prefilter_papers(papers)

    # Generate embeddings for the query and all paper texts
    query_embedding = await embedding_model.aembed_query(query_text)
    paper_embeddings = await embedding_model.aembed_documents([paper_to_text(p) for p in papers])

    # Calculate cosine similarities
    similarities = cosine_similarity(np.array(query_embedding).reshape(1, -1), paper_embeddings).flatten()
    ranked_indices = np.argsort(similarities)[::-1]
    ranked_papers = [
    papers[i]
    for i in ranked_indices
]

    return ranked_papers[:top_k]



