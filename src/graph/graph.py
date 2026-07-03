from langgraph.graph import START, StateGraph
from graph.nodes.summarize_papers import summarize_papers_node
from src.graph.state import GraphState
from src.graph.nodes.generate_queries import generate_queries_node
from src.graph.nodes.search_pubmed import search_pubmed_node
from src.graph.nodes.rank_papers import rank_papers_node
from src.graph.nodes.summarize_papers import summarize_papers_node
from src.graph.nodes.synthesize import synthesize_literature_node
from src.graph.nodes.review import review_literature_synthesis_node
from src.graph.nodes.revise import revise_literature_synthesis_node
from src.graph.nodes.finalize import finalize_review_node
from src.utils.review import should_revise_review
graph=StateGraph(GraphState)

graph.add_node('generate_queries',generate_queries_node)
graph.add_node('search_pubmed', search_pubmed_node)
graph.add_node('rank_papers', rank_papers_node)
graph.add_node('summarize_papers', summarize_papers_node)
graph.add_node('synthesize_literature', synthesize_literature_node)
graph.add_node('review_literature_synthesis', review_literature_synthesis_node)
graph.add_node("revise_literature_synthesis", revise_literature_synthesis_node)
graph.add_node("finalize_review", finalize_review_node)

graph.add_edge(START, 'generate_queries')
graph.add_edge('generate_queries','search_pubmed')
graph.add_edge('search_pubmed', 'rank_papers')
graph.add_edge('rank_papers', 'summarize_papers')
graph.add_edge('summarize_papers', 'synthesize_literature')
graph.add_edge('synthesize_literature', 'review_literature_synthesis')
graph.add_conditional_edges('review_literature_synthesis', 
                            should_revise_review,
                            {
                                "revise": 'revise_literature_synthesis',
                                "finalize": 'finalize_review'
                            })

graph=graph.compile()