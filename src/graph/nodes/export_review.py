from src.services.export import export_markdown

async def export_review_node(state):
    md_path = export_markdown(
        final_review=state["literature_review"],
        citations=state.get("citations", []),
        filename="literature_review",
    )

    return {
        "export_paths": {
            "markdown": md_path
        }
    }