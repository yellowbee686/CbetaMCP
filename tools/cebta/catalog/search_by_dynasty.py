import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_cbeta_by_dynasty(
    dynasty: Annotated[str | None, Field(description="朝代名稱，多個朝代用逗號分隔，如 '唐'、'唐,宋'")] = None,
    time_start: Annotated[int | None, Field(description="起始年份（公元），如 600")] = None,
    time_end: Annotated[int | None, Field(description="結束年份（公元），如 900")] = None,
) -> dict:
    """
    📘 CBETA 朝代/年份搜尋工具
    
    通過朝代名稱或公元時間範圍搜索 CBETA 佛典。
    
    ✅ 兩種搜尋方式（擇一或組合使用）：
    1. dynasty：朝代名稱（支持多個朝代，用英文逗號隔開）
    2. time_start + time_end：公元年範圍
    
    📥 請求範例：
    - dynasty: "唐" → 搜尋唐代佛典
    - dynasty: "唐,宋" → 搜尋唐宋兩朝佛典
    - time_start: 600, time_end: 900 → 搜尋公元600-900年佛典
    
    📤 回應範例：
    {
        "num_found": 1234,
        "sample_result": [
            {
                "work": "T1501",
                "title": "菩薩戒本",
                "byline": "彌勒菩薩說 唐 玄奘譯",
                "time_dynasty": "唐",
                "time_from": 649,
                "time_to": 649,
                "category": "律部類"
            }
        ]
    }
    
    🏷️ 常見朝代：
    - 後漢、三國、西晉、東晉、劉宋、蕭齊、梁、陳
    - 北魏、北齊、北周、隋、唐、五代、北宋、南宋
    - 元、明、清
    """
    if not dynasty and not (time_start and time_end):
        return error_response("請提供 dynasty 或 time_start 與 time_end 參數")

    query_params = {}
    if dynasty:
        query_params["dynasty"] = dynasty
    if time_start:
        query_params["time_start"] = time_start
    if time_end:
        query_params["time_end"] = time_end

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/works", params=query_params)
            resp.raise_for_status()
            data = resp.json()
            return success_response({
                "num_found": data.get("num_found", 0),
                "sample_result": data.get("results", [])[:10]
            })
    except Exception as e:
        return error_response(f"CBETA 查詢失敗: {str(e)}")
