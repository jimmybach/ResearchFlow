

from pathlib import Path
from src.schema.lit_review import LiteratureReview

OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

from src.schema.citations import Citation

def citations_to_markdown(
    citations: list[Citation],
) -> str:

    lines = [
        "# References",
        "",
    ]

    for i, citation in enumerate(citations, start=1):
        lines.append(f"{i}. {citation.apa}")

    return "\n".join(lines)

def citation_link(citation: Citation) -> str:
    return (
        f"- [{citation.title}]{citation.url}")
        



def export_markdown(final_review: LiteratureReview, citations: list[Citation], filename: str):
    path = OUTPUT_DIR / f"{filename}.md"

    citation_text = citations_to_markdown(citations)
    markdown=final_review.to_markdown(citations)
    content = f"""# Literature Review

{markdown}

## References

{citation_text}
"""

    path.write_text(content, encoding="utf-8")

    return str(path)