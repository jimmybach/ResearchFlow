import asyncio

from src.services.mcp.pubmed import pubmed_service
from src.graph.graph import graph
from src.utils.logging import setup_logging
import logging

async def main():
    setup_logging()
    # Initialize external services
    await pubmed_service.initialize()


    # Run the graph
    result = await graph.ainvoke(
        {
            "question": "Exercise and mental health: What is the relationship between physical activity and mental well-being?",
            "revision_count": 0,
            "max_revisions": 2,
            "search_iterations": 0,
            "max_search_iterations": 2
        }
    )

    logger = logging.getLogger(__name__)
    logger.debug(f"Graph execution completed. Result: {result['literature_review']}")



if __name__ == "__main__":
    asyncio.run(main())