from src.utils.pubmed import extract_pmids, extract, parse_paper
from src.schema.paper import Paper
def test_extract_pmids():
    search_result = [
        {
            "text": "**PMIDs:** 12345, 67890, 11111"
        }
    ]

    pmids = extract_pmids(search_result)

    assert pmids == [
        "12345",
        "67890",
        "11111",
    ]

def test_extract():
    text = "**PMID:** 12345\n"

    pmid = extract(
        r"\*\*PMID:\*\*\s*(.*?)\n",
        text,
    )

    assert pmid == "12345"

def test_parse_paper():

    block = """CRISPR Improves Gene Editing

**Authors:** John Smith, Jane Doe

**Journal:** Nature

**PMID:** 123456

**DOI:** 10.1000/test

#### Abstract
This is the abstract.
"""

    paper = parse_paper(block)

    assert paper.pmid == "123456"
    assert paper.title == "CRISPR Improves Gene Editing"
    assert paper.journal == "Nature"
    assert paper.abstract == "This is the abstract."

def test_parse_paper_returns_paper():
    block = """CRISPR Improves Gene Editing

**Authors:** John Smith, Jane Doe

**Journal:** Nature

**PMID:** 123456

**DOI:** 10.1000/test

#### Abstract
This is the abstract.
"""
    paper = parse_paper(block)
    assert isinstance(paper, Paper)
    assert paper.pmid == "123456"
