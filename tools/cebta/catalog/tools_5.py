import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_cbeta_by_dynasty(
    dynasty: Annotated[str | None, Field(description="Dynasty name(s), comma-separated for multiple")] = None,
    time_start: Annotated[int | None, Field(description="Start year in CE")] = None,
    time_end: Annotated[int | None, Field(description="End year in CE")] = None,
) -> dict:
    """
    Search CBETA scriptures by dynasty name or CE year range.
    
    Options:
    - dynasty: dynasty name(s), comma-separated for multiple
    - time_start/time_end: CE year range
    
    At least one parameter must be provided.
    """
    if not dynasty and not (time_start and time_end):
        return error_response("Please provide dynasty or time_start and time_end parameters")

    query_params = {}
    if dynasty:
        query_params["dynasty"] = dynasty
    if time_start:
        query_params["time_start"] = time_start
    if time_end:
        query_params["time_end"] = time_end

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/works", params=query_params)
            resp.raise_for_status()
            data = resp.json()
            return success_response({"num_found": data.get("num_found", 0), "sample_result": data.get("results", [])[:10]})
    except Exception as e:
        return error_response(f"CBETA query failed: {str(e)}")
