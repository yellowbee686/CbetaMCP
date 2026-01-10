import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_facet_query(
    q: Annotated[str, Field(description="Query keyword (required)")],
    f: Annotated[str | None, Field(description="Facet type: canon, category, dynasty, creator, work. If not specified, returns all facets.")] = None,
) -> dict:
    """
    CBETA Facet multi-dimensional query tool.
    
    Query facet structure with 5 categories:
    - canon: Canon ID (e.g. T, X, J)
    - category: Category (e.g. Agama, Mahayana sutras)
    - dynasty: Dynasty (e.g. Tang, Song)
    - creator: Author/translator ID
    - work: Scripture ID (e.g. T01n0001)
    
    Returns facet counts for each category.
    """
    try:
        base_url = "https://api.cbetaonline.cn/search/facet"
        url = f"{base_url}/{f}" if f else base_url

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params={"q": q})
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA facet query failed: {str(e)}")
