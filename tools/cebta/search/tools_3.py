import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def synonym_search(
    q: Annotated[str, Field(description="Query keyword, e.g. '文殊師利'")],
) -> dict:
    """
    CBETA synonym search tool.
    
    Input a keyword and return related synonyms list.
    Useful for text understanding, Q&A, and Buddhist scripture comparison.
    
    Returns:
        - time: query time in seconds
        - num_found: number of synonyms found
        - results: list of synonym terms
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/synonym", params={"q": q})
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"Synonym search failed: {str(e)}")
