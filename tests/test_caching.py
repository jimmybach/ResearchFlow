
from src.services.mcp.pubmed import PubMedService
from src.utils.pubmed import parse_paper


def test_cache_paper_roundtrip(tmp_path):
    service = PubMedService(cache_dir=tmp_path)

    block = """CRISPR Improves Gene Editing

**Authors:** John Smith, Jane Doe

**Journal:** Nature

**PMID:** 123456

**DOI:** 10.1000/test

#### Abstract
This is the abstract.
"""

    paper = parse_paper(block)
    service._cache_paper(paper)

    loaded = service._get_cached_paper(paper.pmid)

    assert loaded == paper