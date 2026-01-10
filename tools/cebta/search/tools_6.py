import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_all_in_one(
    q: Annotated[str, Field(description="Query keyword, supports AND/OR/NOT/NEAR syntax")],
    note: Annotated[int, Field(description="Include annotations: 0=no, 1=yes")] = 1,
    fields: Annotated[str | None, Field(description="Fields to return, e.g. 'work,juan,term_hits'")] = None,
    facet: Annotated[int, Field(description="Return facet: 0=no, 1=yes")] = 0,
    rows: Annotated[int, Field(description="Rows per page")] = 20,
    start: Annotated[int, Field(description="Start position")] = 0,
    around: Annotated[int, Field(description="KWIC context characters")] = 10,
    order: Annotated[str | None, Field(description="Sort order, e.g. 'time_from+' or 'time_from-'")] = None,
    cache: Annotated[int, Field(description="Use cache: 1=yes")] = 1,
) -> dict:
    """
    CBETA All-in-One fulltext search with KWIC and facets.
    
    Returns KWIC (keyword in context) and hit data simultaneously.
    Optionally returns facet (canon, category, creator, dynasty, work) classification.
    Supports AND/OR/NOT/NEAR advanced query syntax.
    """
    try:
        params = {"q": q, "note": note, "facet": facet, "rows": rows, "start": start, "around": around, "cache": cache}
        if fields is not None:
            params["fields"] = fields
        if order is not None:
            params["order"] = order

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/all_in_one", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA all-in-one search failed: {str(e)}")
