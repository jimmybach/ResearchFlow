import re
from src.schema.paper import Paper

def extract_pmids(search_result):
    text = search_result[0]["text"]

    match = re.search(r"\*\*PMIDs:\*\*\s*(.*)", text)

    if not match:
        return []

    return [
        pmid.strip()
        for pmid in match.group(1).split(",")
        if pmid.strip()
    ]

def extract(pattern, text):
    match = re.search(pattern, text, flags=re.DOTALL)

    if match:
        return match.group(1).strip()

    return None

def parse_paper(block: str) -> Paper | None:
    block = block.strip()

    title = extract(r"^(.*?)\n", block)
    pmid = extract(r"\*\*PMID:\*\*\s*(.*?)\n", block)

    if not title or not pmid:
        return None

    authors_text = extract(
        r"\*\*Authors.*?\*\*\s*(.*?)\n\n",
        block,
    )

    authors = (
        [
            line.strip("- ").strip()
            for line in authors_text.splitlines()
            if line.strip()
        ]
        if authors_text
        else []
    )

    return Paper(
        title=title,
        authors=authors,
        journal=extract(r"\*\*Journal:\*\*\s*(.*?)\n", block) or "",
        pmid=pmid,
        doi=extract(r"\*\*DOI:\*\*\s*(.*?)\n", block) or "",
        abstract=extract(r"#### Abstract\n(.*?)(?:\n####|\Z)", block) or "",
    )