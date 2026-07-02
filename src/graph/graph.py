from langgraph.graph import START, StateGraph
from src.graph.state import GraphState
from src.graph.nodes.generate_queries import generate_queries_node
from src.graph.nodes.search_pubmed import search_pubmed_node
from src.graph.nodes.summarize import summarize_node

graph=StateGraph(GraphState)

graph.add_node('generate_queries',generate_queries_node)
graph.add_node('search_pubmed', search_pubmed_node)
graph.add_node('summarize', summarize_node)

graph.add_edge(START, 'generate_queries')
graph.add_edge('generate_queries','search_pubmed')
graph.add_edge('search_pubmed', 'summarize')

graph=graph.compile()