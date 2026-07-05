from src.schema.citations import Citation

def citation_link(citation: Citation) -> str:
    return (
        f"- [{citation.title}]({citation.url})")