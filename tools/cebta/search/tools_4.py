import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_search_sc(
    q: Annotated[str, Field(description="Search keyword (supports Simplified/Traditional Chinese)")],
    fields: Annotated[str | None, Field(description="Limit fields, e.g. 'juan,text'")] = None,
    rows: Annotated[int, Field(description="Number of results to return")] = 10,
    start: Annotated[int, Field(description="Start position")] = 0,
    order: Annotated[str | None, Field(description="Sort order")] = None,
) -> dict:
    """
    CBETA Simplified/Traditional Chinese search tool.
    
    Supports both Simplified and Traditional Chinese input without manual conversion.
    CBETA API handles the conversion automatically.
    """
    try:
        query_params = {"q": q, "rows": rows, "start": start}
        if fields is not None:
            query_params["fields"] = fields
        if order is not None:
            query_params["order"] = order

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/sc", params=query_params)
            resp.raise_for_status()
            data = resp.json()

        return success_response({"q": q, "hits": data.get("hits", 0)})
    except Exception as e:
        return error_response(f"CBETA SC search failed: {str(e)}")
