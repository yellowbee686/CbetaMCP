import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_lines(
    linehead: Annotated[str | None, Field(description="Single line reference, e.g. 'T01n0001_p0001a04'")] = None,
    linehead_start: Annotated[str | None, Field(description="Start line reference for range")] = None,
    linehead_end: Annotated[str | None, Field(description="End line reference for range")] = None,
    before: Annotated[int | None, Field(description="Additional lines before (with linehead)")] = None,
    after: Annotated[int | None, Field(description="Additional lines after (with linehead)")] = None,
) -> dict:
    """
    Get CBETA text lines by linehead reference.
    
    Supports:
    - Single line: linehead
    - Line range: linehead_start + linehead_end
    - Context expansion: linehead + before/after
    
    Returns:
    - linehead: line reference
    - html: HTML content with annotation anchors
    - notes: dictionary of annotation texts
    """
    params = {}
    if linehead:
        params["linehead"] = linehead
    if linehead_start:
        params["linehead_start"] = linehead_start
    if linehead_end:
        params["linehead_end"] = linehead_end
    if before is not None:
        params["before"] = before
    if after is not None:
        params["after"] = after

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/lines", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA line fetch failed: {str(e)}")
