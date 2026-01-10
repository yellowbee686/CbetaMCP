import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_juan_html(
    work: Annotated[str, Field(description="Scripture ID, e.g. 'T0001'")],
    juan: Annotated[int, Field(description="Fascicle number (starting from 1)")],
    work_info: Annotated[int, Field(description="Return scripture info: 0=no, 1=yes")] = 0,
    toc: Annotated[int, Field(description="Return TOC: 0=no, 1=yes")] = 0,
) -> dict:
    """
    Get CBETA fascicle HTML content.
    
    Fetch HTML content for a specific fascicle of a scripture.
    Optionally includes scripture info and table of contents.
    
    Returns:
    - results: list with juan number and HTML content
    - work_info: scripture metadata (if requested)
    - toc: table of contents (if requested)
    """
    try:
        url = "https://api.cbetaonline.cn/juans"
        params = {"work": work, "juan": juan, "work_info": work_info, "toc": toc}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA API request failed: {str(e)}")
