from pydantic import BaseModel
from src.services.formatting import citation_link
from src.schema.citations import Citation
class Theme(BaseModel):
    title: str
    discussion: str
    supporting_pmids: list[str]


class LiteratureReview(BaseModel):
    introduction: str
    major_themes: list[Theme]
    limitations: str
    research_gaps: str
    conclusion: str

    def to_markdown(self, citations: list[Citation]) -> str:
        citation_lookup = {
        citation.pmid: citation
        for citation in citations
        }
        
        sections = []

        sections.append("# Literature Review\n")

        # Introduction
        sections.append("## Introduction\n")
        sections.append(f"{self.introduction}\n")

        # Themes
        sections.append("---\n")
        sections.append("## Major Themes\n")

        for i, theme in enumerate(self.major_themes, start=1):
            sections.append(f"### {i}. {theme.title}\n")
            sections.append(f"{theme.discussion}\n")

            for pmid in theme.supporting_pmids:
                citation = citation_lookup.get(pmid)

                if citation:
                    sections.append(citation_link(citation))

        # Limitations
        sections.append("---\n")
        sections.append("## Limitations\n")
        sections.append(f"{self.limitations}\n")

        # Research gaps
        sections.append("---\n")
        sections.append("## Research Gaps\n")
        sections.append(f"{self.research_gaps}\n")

        # Conclusion
        sections.append("---\n")
        sections.append("## Conclusion\n")
        sections.append(f"{self.conclusion}\n")

        return "\n".join(sections)