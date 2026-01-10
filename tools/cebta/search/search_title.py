import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_title(
    q: Annotated[str, Field(description="搜尋經名關鍵字，至少三個字，如 '觀無量壽經'、'法華經'")],
    rows: Annotated[int, Field(description="每頁筆數")] = 20,
    start: Annotated[int, Field(description="起始位置")] = 0,
) -> dict:
    """
    📘 CBETA 佛典標題（經名）搜尋工具
    
    對佛典經名進行模糊搜尋（至少三個字以上），返回相關書目條目信息。
    
    📥 請求範例：
    - q: "觀無量壽經" → 搜尋經名包含「觀無量壽經」
    - q: "法華經" → 搜尋法華經相關佛典
    - q: "般若波羅蜜" → 搜尋般若波羅蜜相關經典
    
    📤 回應範例：
    {
        "query_string": "觀無量壽經",
        "time": 0.01657838,
        "num_found": 49,
        "results": [
            {
                "work": "X0411",
                "content": "觀無量壽經義疏正觀記",
                "highlight": "<mark>觀無量壽經</mark>義疏正<mark>觀</mark>記",
                "byline": "宋 戒度述",
                "juan": 3,
                "creators_with_id": "戒度(A000511)",
                "time_dynasty": "宋",
                "time_from": 960,
                "time_to": 1279
            }
        ]
    }
    
    🏷️ 返回字段說明：
    - work: 佛典編號
    - content: 經名全稱
    - highlight: 高亮顯示結果
    - byline: 作者資訊
    - juan: 卷數
    - time_dynasty: 朝代
    """
    if len(q.strip()) < 3:
        return error_response("搜尋關鍵字至少需三個字以上")

    try:
        params = {"q": q, "rows": rows, "start": start}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/title", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"標題搜尋失敗: {str(e)}")
