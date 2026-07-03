from langgraph.graph import START, StateGraph
from graph.nodes.summarize_papers import summarize_papers_node
from src.graph.state import GraphState
from src.graph.nodes.generate_queries import generate_queries_node
from src.graph.nodes.search_pubmed import search_pubmed_node
from src.graph.nodes.rank_papers import rank_papers_node
from src.graph.nodes.summarize_papers import summarize_papers_node
from src.graph.nodes.literature_review import review_literature_node
from src.graph.nodes.review_lit_review import review_literature_review_node
from src.graph.nodes.revise_lit_review import revise_literature_review_node
from src.graph.nodes.finalize import finalize_review_node
from src.utils.review import should_revise_review
graph=StateGraph(GraphState)

graph.add_node('generate_queries',generate_queries_node)
graph.add_node('search_pubmed', search_pubmed_node)
graph.add_node('rank_papers', rank_papers_node)
graph.add_node('summarize_papers', summarize_papers_node)
graph.add_node('review_literature', review_literature_node)
graph.add_node('review_lit_review', review_literature_review_node)
graph.add_node("revise_literature_review", revise_literature_review_node)
graph.add_node("finalize_review", finalize_review_node)

graph.add_edge(START, 'generate_queries')
graph.add_edge('generate_queries','search_pubmed')
graph.add_edge('search_pubmed', 'rank_papers')
graph.add_edge('rank_papers', 'summarize_papers')
graph.add_edge('summarize_papers', 'review_literature')
graph.add_edge('review_literature', 'review_lit_review')
graph.add_conditional_edges('review_lit_review', 
                            should_revise_review,
                            {
                                "revise": 'revise_literature_review',
                                "finalize": 'finalize_review'
                            })
graph.add_edge('revise_literature_review', 'review_lit_review')

graph=graph.compile()