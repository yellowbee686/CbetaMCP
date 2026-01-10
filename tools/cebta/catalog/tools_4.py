import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_works_by_translator(
    creator_id: Annotated[str | None, Field(description="Translator ID, e.g. 'A000439'")] = None,
    creator: Annotated[str | None, Field(description="Translator name fuzzy search, e.g. '竺'")] = None,
    creator_name: Annotated[str | None, Field(description="Search only unconfirmed translator names")] = None,
) -> dict:
    """
    Search works by translator/author information.
    
    Three search modes:
    1. By translator ID (creator_id)
    2. Fuzzy search by name (creator)
    3. Search only unconfirmed names (creator_name)
    
    Returns works with title, creators, byline, canon, category, volume, juan count, dynasty, and places.
    """
    url = "https://api.cbetaonline.cn/works"
    query_params = {}

    if creator_id:
        query_params["creator_id"] = creator_id
    elif creator:
        query_params["creator"] = creator
    elif creator_name:
        query_params["creator_name"] = creator_name
    else:
        return error_response("Please provide at least one parameter: creator_id, creator, or creator_name")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"Query failed: {str(e)}")
