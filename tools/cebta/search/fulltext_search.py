import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_fulltext_search(
    q: Annotated[str, Field(description="搜尋關鍵字，如 '法鼓'、'般若波羅蜜'")],
    fields: Annotated[str | None, Field(description="指定回傳欄位，如 'work,juan,term_hits'")] = None,
    rows: Annotated[int, Field(description="每頁回傳筆數")] = 20,
    start: Annotated[int, Field(description="起始位置（用於分頁）")] = 0,
    order: Annotated[str | None, Field(description="排序欄位，如 'time_from-' 依年代降序")] = None,
) -> dict:
    """
    📘 CBETA 一般全文檢索工具
    
    透過 CBETA API 執行佛典全文檢索功能，搜尋包含指定關鍵字的佛典經文。
    
    📥 請求範例：
    - q: "法鼓" → 搜尋包含「法鼓」的佛典
    - q: "般若波羅蜜", rows: 10, order: "time_from-" → 搜尋般若波羅蜜，依年代降序排列
    
    📤 回應範例：
    {
        "query_string": "法鼓",
        "num_found": 2628,
        "total_term_hits": 3860,
        "results": [
            {
                "id": 12298,
                "juan": 1,
                "category": "法華部",
                "canon": "T",
                "vol": "T09",
                "work": "T0270",
                "term_hits": 31,
                "title": "大法鼓經",
                "creators": "求那跋陀羅",
                "file": "T09n0270",
                "time_from": 420,
                "time_to": 479
            }
        ]
    }
    
    🏷️ 返回字段說明：
    - num_found: 符合條件的卷數
    - total_term_hits: 關鍵詞總出現次數
    - results[].juan: 卷號
    - results[].category: 部類
    - results[].canon: 藏經 ID（T=大正藏, X=卍續藏）
    - results[].work: 佛典編號
    - results[].title: 佛典標題
    - results[].term_hits: 該卷關鍵詞出現次數
    - results[].time_from/to: 佛典成立時間
    """
    try:
        query_params = {"q": q, "rows": rows, "start": start}
        if fields:
            query_params["fields"] = fields
        if order:
            query_params["order"] = order
        
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search", params=query_params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA 搜尋失敗: {str(e)}")
