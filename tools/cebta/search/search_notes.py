import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_cbeta_notes(
    q: Annotated[str, Field(description="查詢關鍵詞，需加雙引號，如 '\"法鼓\"'，支援 AND/OR/NOT/NEAR 語法")],
    around: Annotated[int, Field(description="高亮上下文字數")] = 10,
    rows: Annotated[int, Field(description="每頁筆數")] = 20,
    start: Annotated[int, Field(description="起始位置")] = 0,
    facet: Annotated[int, Field(description="是否回傳 facet：0=否，1=是")] = 0,
) -> dict:
    """
    📘 CBETA 註解/校勘搜尋工具
    
    搜尋 CBETA Online 的「註解（夾注、腳註）」內容，支援高亮、分頁與 Facet 統計。
    
    ✅ 查詢語法：
    - AND 查詢："法鼓" "印順"
    - OR 查詢："波羅蜜"|"波羅密"
    - NOT 查詢："迦葉" !"迦葉佛"
    - NEAR 查詢："阿含" NEAR/5 "迦葉"
    
    📥 請求範例：
    - q: '"法鼓"' → 搜尋包含「法鼓」的註解
    - q: '"法鼓"', facet: 1 → 搜尋並返回 facet 統計
    
    📤 回應範例：
    {
        "response": {
            "numFound": 12,
            "start": 0,
            "docs": [
                {
                    "note_place": "foot",
                    "content": "法鼓山創辦人聖嚴法師...",
                    "highlight": "...<mark>法鼓</mark>山創辦人..."
                }
            ]
        },
        "facets": {
            "canon": [{"value": "T", "count": 3}],
            "category": [{"value": "論", "count": 2}],
            "creator": [{"value": "聖嚴", "count": 1}],
            "work": [{"value": "T198", "count": 1}]
        }
    }
    
    🏷️ note_place 說明：
    - "foot"：腳註
    - "inline"：夾注（行內註解）
    """
    try:
        params = {"q": q, "around": around, "rows": rows, "start": start, "facet": facet}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/notes", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA notes 搜尋失敗: {str(e)}")
