import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_title(
    q: Annotated[str, Field(description="Search keyword for scripture title (at least 3 characters)")],
    rows: Annotated[int, Field(description="Rows per page")] = 20,
    start: Annotated[int, Field(description="Start position")] = 0,
) -> dict:
    """
    Search Buddhist scripture titles (sutra names).
    
    Performs fuzzy search on scripture titles (at least 3 characters required).
    Returns bibliography entries including title, volume count, author dynasty info.
    
    Returns:
    - work: book ID
    - content: book title
    - highlight: highlighted result
    - byline: author info
    - juan: volume count
    - creators_with_id: author with ID
    - time_dynasty: dynasty
    - time_from/time_to: year range
    """
    if len(q.strip()) < 3:
        return error_response("Search keyword must be at least 3 characters")

    try:
        params = {"q": q, "rows": rows, "start": start}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/title", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"Title search failed: {str(e)}")
