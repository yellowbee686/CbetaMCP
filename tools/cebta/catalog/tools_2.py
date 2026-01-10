import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_cbeta_texts(
    q: Annotated[str, Field(description="Search keyword or canon volume, e.g. '阿含' or 'T01'")],
) -> dict:
    """
    Search CBETA Buddhist scripture catalog by keyword or volume.
    
    Search scenarios:
    1. Search by keyword (e.g. '阿含')
    2. Search by volume (e.g. 'T01' for Taisho Tripitaka vol.1)
    
    Returns:
    - type: 'catalog' (category), 'work' (scripture title), or 'toc' (table of contents)
    - n: node ID
    - label: display label
    """
    url = "https://api.cbetaonline.cn/toc"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params={"q": q})
            response.raise_for_status()
            return success_response(response.json())
    except httpx.HTTPError as e:
        return error_response(f"HTTP error: {str(e)}")
    except Exception as e:
        return error_response(f"Error: {str(e)}")
