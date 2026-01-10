import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_kwic_search(
    work: Annotated[str, Field(description="Scripture ID, e.g. T0001, X0600")],
    juan: Annotated[int, Field(description="Volume number")],
    q: Annotated[str, Field(description="Query keyword, supports NEAR, exclusion, quotes, comma syntax")],
    note: Annotated[int, Field(description="Include annotations: 0=no, 1=yes")] = 1,
    mark: Annotated[int, Field(description="Add mark tags: 0=no, 1=yes")] = 0,
    sort: Annotated[str, Field(description="Sort: f=after keyword, b=before keyword, location=by position")] = "f",
) -> dict:
    """
    CBETA KWIC (Keyword in Context) single-volume search tool.
    
    Provides context around keywords in a specific scripture volume.
    Supports NEAR queries, word exclusion, annotation toggle, and sorting control.
    
    Returns:
    - num_found: number of hits
    - time: query time in seconds
    - results: list with vol, lb (line position), kwic (context with keywords)
    """
    try:
        params = {"work": work, "juan": juan, "q": q, "note": note, "mark": mark, "sort": sort}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/kwic", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA KWIC search failed: {str(e)}")
