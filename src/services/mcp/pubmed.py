from asyncio.log import logger
import json
from pathlib import Path
import re

from src.utils.pubmed import parse_paper

CACHE_DIR = Path("data/cache/pubmed")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

from langchain_mcp_adapters.client import MultiServerMCPClient
from src.services.mcp.get_tools import get_mcp_tools, get_tool_map
import logging
class PubMedService:

    def __init__(self):
        self.client =  MultiServerMCPClient({
                      "pubmed-mcp-server": {
                        "transport": "http",
                        "url": "https://pubmed.caseyjhand.com/mcp"
                        }
                      })
        self.tool_map = None

    async def initialize(self):
        logger = logging.getLogger(__name__)
        logger.debug("Initializing PubMedService...")
        
        tools = await self.client.get_tools()
        self.tool_map = {
            tool.name: tool
            for tool in tools
        }

    async def search(self, query: str):
        return await self.tool_map["pubmed_search_articles"].ainvoke({'query': query})


    async def fetch(self, pmids: list[str]):
        return await self.tool_map["pubmed_fetch_articles"].ainvoke({'pmids': pmids})
    
    async def fetch_papers_cached(self, pmids: list[str]) -> list[dict]:
      cached_papers = []
      missing_pmids = []

      for pmid in pmids:
          cached = self._get_cached_paper(pmid)

          if cached:
              cached_papers.append(cached)
          else:
              missing_pmids.append(pmid)

      if missing_pmids:
          logger = logging.getLogger(__name__)
          fetch_result = await self.fetch(missing_pmids)

          paper_blocks = re.split(r"\n### ", fetch_result[0]["text"])
          fetched_papers = []
          for paper_block in paper_blocks:
            fetched_papers.append(parse_paper(paper_block))

          for paper in fetched_papers:
              self._cache_paper(paper)
          logger.debug(f"Cached {len(fetched_papers)} new papers for PMIDs: {missing_pmids}")
          cached_papers.extend(fetched_papers)

      return cached_papers
    
    def _cache_path(self, pmid: str) -> Path:
        return CACHE_DIR / f"{pmid}.json"

    def _get_cached_paper(self, pmid: str):
        path = self._cache_path(pmid)

        if not path.exists():
            return None

        with open(path, "r") as f:
            return json.load(f)

    def _cache_paper(self, paper: dict):
        pmid = paper.get("pmid")

        if not pmid:
            return

        path = self._cache_path(pmid)

        with open(path, "w") as f:
            json.dump(paper, f, indent=2)
    
    

pubmed_service = PubMedService()
  


