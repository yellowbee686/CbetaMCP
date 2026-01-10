import httpx
from typing import Annotated
from urllib.parse import quote
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def extended_search(
    q: Annotated[str, Field(description="查詢語句，支援 AND/OR/NOT/NEAR 語法，如 '\"法鼓\" \"聖嚴\"'")],
    start: Annotated[int, Field(description="起始位置")] = 0,
    rows: Annotated[int, Field(description="回傳筆數")] = 20,
) -> dict:
    """
    📘 CBETA 擴充模式全文檢索工具
    
    支援 AND、OR、NOT、NEAR 等進階語法進行全文檢索。
    
    ✅ 查詢語法說明：
    - AND 搜尋：每個詞語加雙引號，空格分隔 → "法鼓" "聖嚴"
    - OR 搜尋：使用 | 運算符 → "波羅蜜" | "波羅密"
    - NOT 搜尋：使用驚嘆號 → "迦葉" !"迦葉佛"
    - NEAR 搜尋：指定距離 → "法鼓" NEAR/7 "迦葉"
    
    📥 請求範例：
    - q: '"法鼓" "聖嚴"' → 同時包含法鼓和聖嚴
    - q: '"波羅蜜" | "波羅密"' → 包含波羅蜜或波羅密
    - q: '"法鼓" NEAR/7 "迦葉"' → 法鼓和迦葉相距7字以內
    
    📤 回應範例：
    {
        "total": 317,
        "rows": [
            {
                "title": "大方廣佛華嚴經",
                "juan": "卷第十",
                "content": "...善財童子至法鼓山..."
            }
        ]
    }
    """
    try:
        encoded_query = quote(q)
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(
                "https://api.cbetaonline.cn/search/extended",
                params={"q": encoded_query, "start": start, "rows": rows},
            )
            resp.raise_for_status()
            data = resp.json()

        total = data.get("total", 0)
        rows_data = [
            {
                "title": r.get("title", ""),
                "juan": r.get("juan", ""),
                "content": r.get("content", ""),
            }
            for r in data.get("results", [])
        ]
        return success_response({"total": total, "rows": rows_data})
    except Exception as e:
        return error_response(f"CBETA 擴充搜尋失敗: {str(e)}")
