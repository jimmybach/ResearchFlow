import re


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

def parse_paper(block):

    return {
        "title": extract(r"^(.*?)\n", block),

        "authors": extract(
            r"\*\*Authors.*?\*\*\s*(.*?)\n\n",
            block,
        ),

        "journal": extract(
            r"\*\*Journal:\*\*\s*(.*?)\n",
            block,
        ),

        "pmid": extract(
            r"\*\*PMID:\*\*\s*(.*?)\n",
            block,
        ),

        "doi": extract(
            r"\*\*DOI:\*\*\s*(.*?)\n",
            block,
        ),

        "abstract": extract(
            r"#### Abstract\n(.*?)(?:\n####|\Z)",
            block,
        ),
    }

