# app/streamlit_app.py

import asyncio
import sys
from pathlib import Path
import time

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.graph.graph import graph
from src.services.mcp.pubmed import pubmed_service
from src.utils.logging import setup_logging
from src.utils.ui import render_paper_card


st.set_page_config(
    page_title="ResearchFlow",
    page_icon="🧬",
    layout="wide",
)

NODE_ORDER = [
    "generate_queries",
    "search_pubmed",
    "rank_papers",
    "analyze_coverage",
    "search_followup_pubmed",
    "summarize_papers",
    "cite_papers",
    "review_literature",
    "review_lit_review",
    "revise_literature_review",
    "finalize_review",
    "export_review",
]

NODE_LABELS = {
    "generate_queries": "Generate queries",
    "search_pubmed": "Search PubMed",
    "rank_papers": "Rank papers",
    "analyze_coverage": "Analyze coverage",
    "search_followup_pubmed": "Follow-up search",
    "summarize_papers": "Summarize papers",
    "cite_papers": "Generate citations",
    "review_literature": "Synthesize review",
    "review_lit_review": "Critique review",
    "revise_literature_review": "Revise review",
    "finalize_review": "Finalize review",
    "export_review": "Export results",
}


def render_workflow_panel(placeholder, completed_nodes=None, active_node=None):
    completed_nodes = completed_nodes or []

    lines = ["### Workflow Progress", ""]

    for node in NODE_ORDER:
        label = NODE_LABELS[node]

        if node == active_node:
            icon = "🟡"
        elif node in completed_nodes:
            icon = "🟢"
        else:
            icon = "⚪"

        lines.append(f"{icon} {label}")

    placeholder.markdown("\n\n".join(lines))


async def run_researchflow_with_status(
    question,
    workflow_placeholder,
    top_k,
    max_search_iterations,
    max_revisions,
):
    input_state = {
        "question": question,
        "revision_count": 0,
        "max_revisions": max_revisions,
        "search_iterations": 0,
        "max_search_iterations": max_search_iterations,
        "top_k": top_k,
    }

    await pubmed_service.initialize()

    result = {}
    completed_nodes = []

    render_workflow_panel(workflow_placeholder, completed_nodes)

    async for event in graph.astream(input_state):
        for node_name, node_output in event.items():
            render_workflow_panel(
                workflow_placeholder,
                completed_nodes=completed_nodes,
                active_node=node_name,
            )

            completed_nodes.append(node_name)

            render_workflow_panel(
                workflow_placeholder,
                completed_nodes=completed_nodes,
            )

            if isinstance(node_output, dict):
                result.update(node_output)

    result["completed_nodes"] = completed_nodes
    return result


def get_or_create_event_loop():
    if "event_loop" not in st.session_state:
        st.session_state["event_loop"] = asyncio.new_event_loop()

    return st.session_state["event_loop"]


def run_async(coro):
    loop = get_or_create_event_loop()
    return loop.run_until_complete(coro)


setup_logging()

with st.sidebar:
    st.header("Settings")

    max_revisions = st.slider("Max review revisions", 0, 3, 1)
    max_search_iterations = st.slider("Max search iterations", 0, 3, 1)
    top_k = st.slider("Papers to summarize", 5, 50, 1)

    st.divider()
    st.header("Run Statistics")

    result = st.session_state.get("result")

    if result:
        st.metric("Papers retrieved", len(result.get("papers", [])))
        st.metric("Ranked papers", len(result.get("ranked_papers", [])))
        st.metric("Summaries", len(result.get("paper_summaries", [])))
        st.metric("Search iterations", result.get("search_iterations", 0))
        st.metric("Review revisions", result.get("revision_count", 0))
        st.metric("Execution time", f"{result.get('execution_time_seconds', 0):.1f}s")
    else:
        st.info("Run a review to see statistics.")

st.title("ResearchFlow")
st.caption("Agentic literature review assistant for biomedical research")

examples = [
    "What are the effects of physical activity on depression?",
    "What are recent advances in CRISPR gene editing specificity?",
    "What factors predict childhood vaccination uptake in low-resource settings?",
]

example = st.selectbox("Try an example", [""] + examples)

question = st.text_area(
    "Research question",
    value=example,
    placeholder="Enter a biomedical research question...",
    height=120,
)

run_button = st.button("Generate Literature Review", type="primary")

st.divider()

workflow_col, results_col = st.columns([1, 3])

with workflow_col:
    workflow_placeholder = st.empty()

    completed_nodes = st.session_state.get("result", {}).get("completed_nodes", [])
    render_workflow_panel(workflow_placeholder, completed_nodes)

with results_col:
    tab_review, tab_papers, tab_citations, tab_exports = st.tabs(
        ["Review", "Papers", "Citations", "Exports"]
    )

    result = st.session_state.get("result")

    with tab_review:
        st.subheader("Literature Review")

        if not result:
            st.info("Generated literature review will appear here.")
        else:
            final_review = result.get("final_review") or result.get("literature_review")

            if final_review is None:
                st.warning("No literature review found.")
            elif hasattr(final_review, "to_markdown"):
                st.markdown(final_review.to_markdown(result.get("citations", [])))
            else:
                st.markdown(str(final_review))

    with tab_papers:
        st.subheader("Ranked Papers")

        papers = result.get("ranked_papers", [])

        if not result:
            st.info("Ranked papers will appear here.")
        elif not papers:
            st.info("No ranked papers found.")
        else:
            for paper in papers:
                render_paper_card(paper)

    with tab_citations:
        st.subheader("Citations")

        if not result:
            st.info("Citations will appear here.")
        else:
            citations = result.get("citations", [])

            if not citations:
                st.info("No citations found.")
            else:
                for citation in citations:
                    st.markdown(f"- {citation.apa}")

    with tab_exports:
        st.subheader("Downloads")

        if not result:
            st.info("Downloads will appear here.")
        else:
            export_paths = result.get("export_paths", {})
            md_path = export_paths.get("markdown")

            if md_path and Path(md_path).exists():
                markdown_text = Path(md_path).read_text(encoding="utf-8")

                st.download_button(
                    label="Download Markdown",
                    data=markdown_text,
                    file_name="literature_review.md",
                    mime="text/markdown",
                )
            else:
                st.info("No export file found.")

if run_button:
    if not question.strip():
        st.warning("Enter a research question first.")
    else:
        start_time = time.time()

        result = run_async(
            run_researchflow_with_status(
                question=question,
                workflow_placeholder=workflow_placeholder,
                max_search_iterations=max_search_iterations,
                max_revisions=max_revisions,
                top_k=top_k,
            )
        )

        result["execution_time_seconds"] = time.time() - start_time

        st.session_state["result"] = result
        st.rerun()
