import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_catalog(
    q: Annotated[str, Field(description="Query node ID, e.g. 'root', 'CBETA', 'orig-T', 'CBETA.001'")],
) -> dict:
    """
    Query CBETA Online catalog structure data.
    
    Query types (q parameter):
    - "root": get all top-level directory nodes
    - "CBETA": get CBETA category catalog (e.g. Agama, Prajna, etc.)
    - "orig": get all original canon classifications
    - "orig-T": get Taisho Tripitaka structure catalog
    - "CBETA.001": get detailed catalog under a specific category
    
    Returns results with 'n' (node ID) and 'label' fields that can be used for further queries.
    """
    url = "https://api.cbetaonline.cn/catalog_entry"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params={"q": q})
            response.raise_for_status()
            return success_response(response.json())
    except httpx.HTTPError as e:
        return error_response(f"HTTP error: {str(e)}")
    except Exception as e:
        return error_response(f"Error: {str(e)}")
