import streamlit as st

def render_paper_card(paper):
    title = getattr(paper, "title", "Untitled paper")
    pmid = getattr(paper, "pmid", None)
    journal = getattr(paper, "journal", "Unknown journal")
    doi = getattr(paper, "doi", None)
    abstract = getattr(paper, "abstract", None)
    score = getattr(paper, "relevance_score", None)

    with st.container(border=True):
        st.markdown(f"### {title}")

        meta = []

        if journal:
            meta.append(f"**Journal:** {journal}")

        if pmid:
            meta.append(
                f"**PMID:** [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)"
            )

        if doi:
            meta.append(f"**DOI:** {doi}")

        if score is not None:
            meta.append(f"**Score:** {score:.3f}")

        st.markdown("  \n".join(meta))

        if abstract:
            with st.expander("Abstract"):
                st.write(abstract)