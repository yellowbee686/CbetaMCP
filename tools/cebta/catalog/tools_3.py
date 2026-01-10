import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_buddhist_canons_by_vol(
    canon: Annotated[str, Field(description="Canon ID, e.g. 'T' or 'X'")],
    vol_start: Annotated[int, Field(description="Start volume number")],
    vol_end: Annotated[int, Field(description="End volume number")],
) -> dict:
    """
    Search Buddhist scriptures by canon and volume range.
    
    Query scriptures within a specified canon (canon) ID and volume range.
    
    Example: canon='T', vol_start=1, vol_end=2 returns scriptures in Taisho vol.1-2
    
    Returns:
    - work: scripture ID
    - title: scripture title
    - vol: volume ID
    - juan: number of fascicles
    - byline: translator info
    """
    url = "https://api.cbetaonline.cn/works"
    query_params = {"canon": canon, "vol_start": vol_start, "vol_end": vol_end}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            data = resp.json()
            return success_response({"num_found": data.get("num_found"), "results": data.get("results", [])})
    except Exception as e:
        return error_response(f"API request failed: {str(e)}")
