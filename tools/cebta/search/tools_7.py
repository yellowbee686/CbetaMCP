import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_cbeta_notes(
    q: Annotated[str, Field(description="Query keyword with quotes, e.g. '\"法鼓\"'. Supports AND/OR/NOT/NEAR syntax.")],
    around: Annotated[int, Field(description="Highlight context characters")] = 10,
    rows: Annotated[int, Field(description="Rows per page")] = 20,
    start: Annotated[int, Field(description="Start position")] = 0,
    facet: Annotated[int, Field(description="Return facet: 0=no, 1=yes")] = 0,
) -> dict:
    """
    CBETA notes/collation search tool.
    
    Search annotation content (inline notes, footnotes) in CBETA Online.
    Supports highlight, pagination and facet statistics.
    
    Query syntax:
    - AND: "法鼓" "印順"
    - OR: "波羅蜜"|"波羅密"
    - NOT: "迦葉" !"迦葉佛"
    - NEAR: "阿含" NEAR/5 "迦葉"
    
    Returns:
    - content: actual note text
    - note_place: note position ("foot" or "inline")
    - highlight: context snippet with keyword
    - facets (if facet=1): canon, category, creator, work statistics
    """
    try:
        params = {"q": q, "around": around, "rows": rows, "start": start, "facet": facet}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/notes", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA notes search failed: {str(e)}")
