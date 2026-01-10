import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response

# 📘 CBETA 一般全文檢索工具
# 說明：
# 本工具透過 CBETA API 執行佛典全文檢索功能。
# 可輸入關鍵字與查詢選項（欄位、筆數、排序等），回傳包含卷號、藏經 ID、佛典編號等資訊。


@__mcp_server__.tool
async def cbeta_fulltext_search(
    q: Annotated[str, Field(description="Search keyword (required)")],
    fields: Annotated[str | None, Field(description="Fields to return, e.g. 'work,juan,term_hits'")] = None,
    rows: Annotated[int, Field(description="Number of rows per page")] = 20,
    start: Annotated[int, Field(description="Start position")] = 0,
    order: Annotated[str | None, Field(description="Order by field, e.g. 'time_from-' for descending by time")] = None,
) -> dict:
    """
    CBETA fulltext search tool using CBETA Open API.
    
    Returns:
        - num_found: number of matching volumes
        - total_term_hits: total keyword occurrences
        - results: list of results with juan, category, canon, vol, work, title, creators, file, time_from/to
    
    Doc: https://api.cbetaonline.cn/search
    """
    try:
        query_params = {"q": q}
        if fields is not None:
            query_params["fields"] = fields
        if rows != 20:
            query_params["rows"] = rows
        if start != 0:
            query_params["start"] = start
        if order is not None:
            query_params["order"] = order
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search", params=query_params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA search failed: {str(e)}")
