import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_toc(
    work: Annotated[str, Field(description="Scripture ID, e.g. 'T0001'")],
) -> dict:
    """
    Get CBETA scripture table of contents structure.
    
    Returns hierarchical TOC with:
    - title: section title
    - file: XML file name
    - juan: fascicle number
    - lb: page/column/line position
    - type: node type (序, 分, 經, etc.)
    - n: node sequence number
    - isFolder: whether has children
    - children: sub-nodes
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get("https://api.cbetaonline.cn/toc", params={"work": work})
            response.raise_for_status()
            return success_response(response.json())
    except Exception as e:
        return error_response(f"Failed to get CBETA TOC: {str(e)}")
