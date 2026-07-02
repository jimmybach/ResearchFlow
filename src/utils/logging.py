import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    noisy_loggers = [
            "httpx",
            "httpcore",
            "google_genai",
            "google_genai.models",
            "mcp",
            "mcp.client",
            "mcp.client.streamable_http",
            "langchain",
            "langgraph",
            "langsmith",
        ]

    for name in noisy_loggers:
        logging.getLogger(name).setLevel(logging.WARNING)
