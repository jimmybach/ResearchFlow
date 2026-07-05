from langgraph.graph import START, StateGraph, END
from src.graph.nodes.summarize_papers import summarize_papers_node
from src.graph.state import GraphState
from src.graph.nodes.generate_queries import generate_queries_node
from src.graph.nodes.search_pubmed import search_pubmed_node
from src.graph.nodes.rank_papers import rank_papers_node
from src.graph.nodes.analyze_coverage import analyze_coverage_node
from src.graph.nodes.search_followup_pubmed import search_followup_pubmed_node
from src.graph.nodes.cite_papers import cite_papers_node
from src.graph.nodes.summarize_papers import summarize_papers_node
from src.graph.nodes.literature_review import review_literature_node
from src.graph.nodes.review_lit_review import review_literature_review_node
from src.graph.nodes.revise_lit_review import revise_literature_review_node
from src.graph.nodes.finalize import finalize_review_node
from src.graph.nodes.export_review import export_review_node
from src.utils.routing import should_revise_review, should_search_more
build=StateGraph(GraphState)

build.add_node('generate_queries',generate_queries_node)
build.add_node('search_pubmed', search_pubmed_node)
build.add_node('rank_papers', rank_papers_node)
build.add_node('analyze_coverage', analyze_coverage_node)
build.add_node('search_followup_pubmed', search_followup_pubmed_node)
build.add_node('cite_papers', cite_papers_node)
build.add_node('summarize_papers', summarize_papers_node)
build.add_node('review_literature', review_literature_node)
build.add_node('review_lit_review', review_literature_review_node)
build.add_node("revise_literature_review", revise_literature_review_node)
build.add_node("finalize_review", finalize_review_node)
build.add_node('export_review', export_review_node)



build.add_edge(START, 'generate_queries')
build.add_edge('generate_queries','search_pubmed')
build.add_edge('search_pubmed', 'rank_papers')
build.add_edge('rank_papers','analyze_coverage')
build.add_conditional_edges('analyze_coverage',
                            should_search_more,
                            {'summarize_papers':'summarize_papers',
                             'search_more': 'search_followup_pubmed'})

build.add_edge('search_followup_pubmed', 'rank_papers')
build.add_edge('summarize_papers','cite_papers')
build.add_edge("cite_papers", "review_literature")
build.add_edge('review_literature', 'review_lit_review')
build.add_conditional_edges('review_lit_review', 
                            should_revise_review,
                            {
                                "revise": 'revise_literature_review',
                                "finalize": 'finalize_review'
                            })
build.add_edge('revise_literature_review', 'review_lit_review')
build.add_edge('finalize_review', 'export_review')
build.add_edge('export_review', END)
graph=build.compile()