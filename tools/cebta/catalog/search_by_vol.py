import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_buddhist_canons_by_vol(
    canon: Annotated[str, Field(description="藏經 ID，如 'T'（大正藏）、'X'（卍續藏）、'J'（嘉興藏）")],
    vol_start: Annotated[int, Field(description="開始冊數")],
    vol_end: Annotated[int, Field(description="結束冊數")],
) -> dict:
    """
    📘 CBETA 佛典範圍搜尋工具
    
    根據指定藏經 ID 與冊數起迄範圍，查詢對應範圍內的佛典資料。
    
    📥 請求範例：
    - canon: "T", vol_start: 1, vol_end: 2 → 大正藏第1-2冊
    - canon: "X", vol_start: 1, vol_end: 5 → 卍續藏第1-5冊
    
    📤 回應範例：
    {
        "num_found": 155,
        "results": [
            {
                "work": "T0001",
                "title": "長阿含經",
                "vol": "T01",
                "juan": 22,
                "byline": "後秦 佛陀耶舍共竺佛念譯",
                "category": "阿含部類",
                "time_dynasty": "後秦",
                "time_from": 412,
                "time_to": 413
            },
            {
                "work": "T0002",
                "title": "七佛經",
                "vol": "T01",
                "juan": 1
            }
        ]
    }
    
    🏷️ 常用藏經 ID：
    - T：大正藏
    - X：卍續藏
    - J：嘉興藏
    - N：南傳大藏經
    """
    url = "https://api.cbetaonline.cn/works"
    query_params = {"canon": canon, "vol_start": vol_start, "vol_end": vol_end}

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            data = resp.json()
            return success_response({
                "num_found": data.get("num_found"),
                "results": data.get("results", [])
            })
    except Exception as e:
        return error_response(f"API 請求失敗: {str(e)}")
