# app/streamlit_app.py

import asyncio
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.graph.graph import graph
from src.services.mcp.pubmed import pubmed_service
from src.utils.logging import setup_logging


st.set_page_config(
    page_title="ResearchFlow",
    page_icon="🧬",
    layout="wide",
)


async def run_researchflow(question: str):
    await pubmed_service.initialize()

    result = await graph.ainvoke(
        {
            "question": question,
            "revision_count": 0,
            "max_revisions": 3,
            "search_iterations": 0,
            "max_search_iterations": 3,
        }
    )

    return result


def run_async(coro):
    return asyncio.run(coro)


setup_logging()

st.title("ResearchFlow")
st.caption("Agentic literature review assistant for biomedical research")

question = st.text_area(
    "Research question",
    placeholder="Example: What are the effects of physical activity on mental health?",
    height=120,
)

run_button = st.button("Generate Literature Review", type="primary")

if run_button:
    if not question.strip():
        st.warning("Enter a research question first.")
    else:
        with st.status("Running ResearchFlow...", expanded=True) as status:
            st.write("Generating search queries...")
            st.write("Searching PubMed...")
            st.write("Ranking papers...")
            st.write("Analyzing coverage...")
            st.write("Summarizing papers...")
            st.write("Synthesizing review...")
            st.write("Critiquing and revising...")
            st.write("Exporting results...")

            result = run_async(run_researchflow(question))

            status.update(
                label="ResearchFlow complete",
                state="complete",
                expanded=False,
            )

        st.session_state["result"] = result


if "result" in st.session_state:
    result = st.session_state["result"]

    st.divider()

    tab_review, tab_papers, tab_citations, tab_exports = st.tabs(
        ["Review", "Papers", "Citations", "Exports"]
    )

    with tab_review:
        st.subheader("Literature Review")

        final_review = result.get("literature_review")

        if hasattr(final_review, "to_markdown"):
            st.markdown(final_review.to_markdown(result.get('citations')))
        else:
            st.markdown(str(final_review))

    with tab_papers:
        st.subheader("Ranked Papers")

        ranked_papers = result.get("ranked_papers", [])

        for paper in ranked_papers:
            with st.expander(paper.title):
                st.write(f"**PMID:** {paper.pmid}")
                st.write(f"**Journal:** {paper.journal}")
                st.write(f"**DOI:** {paper.doi}")
                st.write(paper.abstract)

    with tab_citations:
        st.subheader("Citations")

        citations = result.get("citations", [])

        for citation in citations:
            st.markdown(f"- {citation.apa}")

    with tab_exports:
        st.subheader("Downloads")

        export_paths = result.get("export_paths", {})

        md_path = export_paths.get("markdown")

        if md_path and Path(md_path).exists():
            with open(md_path, "r", encoding="utf-8") as f:
                markdown_text = f.read()

            st.download_button(
                label="Download Markdown",
                data=markdown_text,
                file_name="literature_review.md",
                mime="text/markdown",
            )
        else:
            st.info("No export file found.")
    st.write("Result keys:", list(result.keys()))
    st.write("Export paths:", result.get("export_paths"))