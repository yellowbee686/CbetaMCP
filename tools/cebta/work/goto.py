import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_goto(
    canon: Annotated[str | None, Field(description="藏經編號，如 'T'（大正藏）、'X'（卍續藏）、'N'（南傳）")] = None,
    work: Annotated[str | None, Field(description="經號，如 '1'、'2'、'150A'")] = None,
    juan: Annotated[int | None, Field(description="卷數")] = None,
    vol: Annotated[int | None, Field(description="冊數")] = None,
    page: Annotated[int | None, Field(description="頁碼")] = None,
    col: Annotated[str | None, Field(description="欄位：'a'、'b'、'c'")] = None,
    line: Annotated[int | None, Field(description="行數")] = None,
    linehead: Annotated[str | None, Field(description="行首引用，如 'T01n0001_p0066c25'（優先使用）")] = None,
) -> dict:
    """
    📘 CBETA 經文位置跳轉工具
    
    封裝 CBETA Online 的 /juans/goto 接口，支持多種方式跳轉到經文位置。
    
    ✅ 三種跳轉模式：
    1. 經卷結構：canon + work + (juan/page/col/line)
    2. 書本結構：canon + vol + (page/col/line)
    3. 行首引用：linehead（優先級最高）
    
    📥 請求範例：
    - linehead: "T01n0001_p0066c25" → 直接跳轉到該行
    - canon: "T", work: "1", page: 11, col: "b", line: 10 → 大正藏第1經第11頁b欄第10行
    - canon: "T", vol: 1, page: 11, col: "b", line: 10 → 大正藏第1冊第11頁b欄第10行
    
    📤 回應範例：
    {
        "url": "https://cbetaonline.cn/zh/T01n0001_p0066c25"
    }
    
    ⚠️ 注意：若提供 linehead，則其他參數將被忽略。
    """
    base_url = "https://api.cbetaonline.cn/juans/goto"
    query_params = {}

    if linehead:
        query_params["linehead"] = linehead
    else:
        if canon:
            query_params["canon"] = canon
        if work:
            query_params["work"] = work
        if juan is not None:
            query_params["juan"] = juan
        if vol is not None:
            query_params["vol"] = vol
        if page is not None:
            query_params["page"] = page
        if col:
            query_params["col"] = col
        if line is not None:
            query_params["line"] = line

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(base_url, params=query_params)
            response.raise_for_status()
            return success_response({"url": str(response.url)})
    except Exception as e:
        return error_response(f"CBETA 跳轉失敗：{str(e)}")
