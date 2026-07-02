from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_mcp_tools(client: MultiServerMCPClient):

  return await client.get_tools()


def get_tool_map(tools):
    return {tool.name: tool for tool in tools}