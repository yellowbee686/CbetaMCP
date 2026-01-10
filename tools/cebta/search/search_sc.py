import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_search_sc(
    q: Annotated[str, Field(description="搜尋關鍵字，支持簡體或繁體，如 '四圣谛' 或 '四聖諦'")],
    fields: Annotated[str | None, Field(description="限定欄位，如 'juan,text'")] = None,
    rows: Annotated[int, Field(description="回傳筆數")] = 10,
    start: Annotated[int, Field(description="起始位置")] = 0,
    order: Annotated[str | None, Field(description="排序方式")] = None,
) -> dict:
    """
    📘 CBETA 簡體/繁體搜尋工具
    
    支持簡體或繁體中文輸入，CBETA 會自動處理簡繁轉換，無需手動轉換。
    
    📥 請求範例：
    - q: "四圣谛" → 用簡體搜尋「四聖諦」
    - q: "般若波罗蜜" → 用簡體搜尋「般若波羅蜜」
    - q: "四聖諦" → 直接用繁體搜尋
    
    📤 回應範例：
    {
        "q": "四圣谛",
        "hits": 41
    }
    
    🏷️ 說明：
    此工具適合用戶使用簡體中文輸入時，自動匹配繁體佛典內容。
    """
    try:
        query_params = {"q": q, "rows": rows, "start": start}
        if fields:
            query_params["fields"] = fields
        if order:
            query_params["order"] = order

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/sc", params=query_params)
            resp.raise_for_status()
            data = resp.json()

        return success_response({"q": q, "hits": data.get("hits", 0)})
    except Exception as e:
        return error_response(f"CBETA SC 搜尋失敗: {str(e)}")
