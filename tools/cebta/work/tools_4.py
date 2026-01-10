import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_goto(
    canon: Annotated[str | None, Field(description="Canon ID, e.g. 'T', 'X', 'N'")] = None,
    work: Annotated[str | None, Field(description="Scripture number, e.g. '1', '150A'")] = None,
    juan: Annotated[int | None, Field(description="Fascicle number")] = None,
    vol: Annotated[int | None, Field(description="Volume number")] = None,
    page: Annotated[int | None, Field(description="Page number")] = None,
    col: Annotated[str | None, Field(description="Column: a, b, or c")] = None,
    line: Annotated[int | None, Field(description="Line number")] = None,
    linehead: Annotated[str | None, Field(description="Linehead reference, e.g. 'T01n0001_p0066c25'")] = None,
) -> dict:
    """
    Navigate to CBETA scripture text position URL.
    
    Three navigation modes:
    1. canon + work + (juan/page/col/line)
    2. canon + vol + (page/col/line)
    3. linehead (takes priority if provided)
    
    Note: If linehead is provided, other parameters are ignored.
    """
    base_url = "https://api.cbetaonline.cn/juans/goto"
    query_params = {}

    if linehead:
        query_params["linehead"] = linehead
    else:
        if canon:
            query_params["canon"] = canon
        if work:
            query_params["work"] = work
        if juan is not None:
            query_params["juan"] = juan
        if vol is not None:
            query_params["vol"] = vol
        if page is not None:
            query_params["page"] = page
        if col:
            query_params["col"] = col
        if line is not None:
            query_params["line"] = line

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(base_url, params=query_params)
            response.raise_for_status()
            return success_response({"url": str(response.url)})
    except Exception as e:
        return error_response(f"CBETA navigation failed: {str(e)}")
