import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_works_by_translator(
    creator_id: Annotated[str | None, Field(description="作譯者 ID，如 'A000439'（玄奘）")] = None,
    creator: Annotated[str | None, Field(description="作譯者姓名模糊搜尋，如 '玄奘'、'鳩摩羅什'")] = None,
    creator_name: Annotated[str | None, Field(description="僅搜尋尚未確認 ID 的譯者姓名")] = None,
) -> dict:
    """
    📘 CBETA 作譯者搜尋工具
    
    根據作譯者資訊搜尋佛典作品。
    
    ✅ 三種搜尋方式（擇一使用）：
    1. creator_id：指定作譯者 ID 精確搜尋
    2. creator：作譯者姓名模糊搜尋
    3. creator_name：僅搜尋尚未確認 ID 的姓名
    
    📥 請求範例：
    - creator_id: "A000439" → 搜尋玄奘的譯作
    - creator: "玄奘" → 模糊搜尋包含「玄奘」的譯者
    - creator: "鳩摩羅什" → 搜尋鳩摩羅什的譯作
    
    📤 回應範例：
    {
        "num_found": 6,
        "results": [
            {
                "work": "T0001",
                "title": "長阿含經",
                "creators": "佛陀耶舍,竺佛念",
                "creators_with_id": "佛陀耶舍(A000439);竺佛念(A000435)",
                "byline": "後秦 佛陀耶舍共竺佛念譯",
                "canon": "T",
                "category": "阿含部類",
                "vol": "T01",
                "juan": 22,
                "time_dynasty": "後秦",
                "time_from": 412,
                "time_to": 413,
                "places": [
                    {"name": "長安", "latitude": 34.3288, "longitude": 108.9064}
                ]
            }
        ]
    }
    """
    url = "https://api.cbetaonline.cn/works"
    query_params = {}

    if creator_id:
        query_params["creator_id"] = creator_id
    elif creator:
        query_params["creator"] = creator
    elif creator_name:
        query_params["creator_name"] = creator_name
    else:
        return error_response("請至少提供一個搜尋參數：creator_id、creator 或 creator_name")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params=query_params)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "error" in data:
                error = data["error"]
                if isinstance(error, dict):
                    message = error.get("message", "CBETA API returned an error")
                else:
                    message = str(error)
                return error_response(f"CBETA API error: {message}")
            return success_response(data)
    except Exception as e:
        return error_response(f"查詢失敗: {str(e)}")
