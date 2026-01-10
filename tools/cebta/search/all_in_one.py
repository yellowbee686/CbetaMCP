import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_all_in_one(
    q: Annotated[str, Field(description="查詢關鍵字，支援 AND/OR/NOT/NEAR 語法")],
    note: Annotated[int, Field(description="是否含夾注：0=不含，1=含")] = 1,
    fields: Annotated[str | None, Field(description="回傳欄位，如 'work,juan,term_hits'")] = None,
    facet: Annotated[int, Field(description="是否回傳 facet：0=否，1=是")] = 0,
    rows: Annotated[int, Field(description="每頁筆數")] = 20,
    start: Annotated[int, Field(description="起始位置")] = 0,
    around: Annotated[int, Field(description="KWIC 前後字數")] = 10,
    order: Annotated[str | None, Field(description="排序條件，如 'time_from+' 升序，'time_from-' 降序")] = None,
    cache: Annotated[int, Field(description="是否使用快取：1=是")] = 1,
) -> dict:
    """
    📘 CBETA 全文檢索 All-in-One 工具
    
    查詢關鍵字後，同時回傳 KWIC（關鍵字前後文段）與命中資料。
    可選擇是否同時返回 Facet 分類資訊。支援進階語法查詢。
    
    📥 請求範例：
    - q: "法鼓" → 基本搜尋
    - q: "法鼓", facet: 1 → 搜尋並返回 facet 分類
    - q: "法鼓", around: 20 → 擴大 KWIC 前後文範圍
    
    📤 回應範例（不含 facet）：
    {
        "query_string": "法鼓",
        "num_found": 1059,
        "total_term_hits": 1492,
        "results": [
            {
                "juan": 1,
                "canon": "T",
                "work": "T0270",
                "title": "大法鼓經",
                "term_hits": 31,
                "kwics": {
                    "num_found": 31,
                    "results": [
                        {"kwic": "擊於大<mark>法鼓</mark>..."}
                    ]
                }
            }
        ]
    }
    
    📤 回應範例（含 facet）：
    {
        "facet": {
            "category": [
                {"category_id": 17, "category_name": "禪宗部類", "juans": 283}
            ],
            "dynasty": [
                {"dynasty": "唐", "juans": 164}
            ]
        }
    }
    
    🏷️ KWIC 說明：
    KWIC = Keyword In Context，顯示關鍵字在經文中的上下文。
    <mark>...</mark> 標記關鍵字位置。
    """
    try:
        params = {"q": q, "note": note, "facet": facet, "rows": rows, "start": start, "around": around, "cache": cache}
        if fields:
            params["fields"] = fields
        if order:
            params["order"] = order

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/all_in_one", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA all-in-one 搜尋失敗: {str(e)}")
