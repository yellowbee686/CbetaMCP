import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_lines(
    linehead: Annotated[str | None, Field(description="指定單行行號，如 'T01n0001_p0001a04'")] = None,
    linehead_start: Annotated[str | None, Field(description="行段起始行號")] = None,
    linehead_end: Annotated[str | None, Field(description="行段結束行號")] = None,
    before: Annotated[int | None, Field(description="額外取得前幾行（搭配 linehead 使用）")] = None,
    after: Annotated[int | None, Field(description="額外取得後幾行（搭配 linehead 使用）")] = None,
) -> dict:
    """
    📘 CBETA 指定行段文字取得工具
    
    透過 CBETA Online API，依據「行首資訊」取得大正藏對應行文字（含註解）。
    
    ✅ 支援三種模式：
    1. 單行：linehead
    2. 行段範圍：linehead_start + linehead_end
    3. 上下文擴展：linehead + before/after
    
    📥 請求範例：
    - linehead: "T01n0001_p0001a04" → 取得該單行
    - linehead: "T01n0001_p0001a04", before: 2, after: 3 → 取得該行及前2後3行
    - linehead_start: "T01n0001_p0001a04", linehead_end: "T01n0001_p0001a10" → 取得行段範圍
    
    📤 回應範例：
    {
        "num_found": 1,
        "results": [
            {
                "linehead": "T01n0001_p0001a04",
                "html": "<a class=\"noteAnchor\" href=\"#n0001002\"></a>長安釋僧肇<a class=\"noteAnchor\" href=\"#n0001003\"></a>述",
                "notes": {
                    "0001002": "〔長安〕－【宋】",
                    "0001003": "〔述〕－【宋】"
                }
            }
        ]
    }
    
    🏷️ 返回字段說明：
    - linehead: 行首位置標識
    - html: 該行 HTML 內容（含註解錨點）
    - notes: 註解內容字典（key 為註解 ID，value 為註解文字）
    
    🔗 行首格式說明：T01n0001_p0001a04 = 大正藏第1冊第1經第1頁a欄第4行
    """
    params = {}
    if linehead:
        params["linehead"] = linehead
    if linehead_start:
        params["linehead_start"] = linehead_start
    if linehead_end:
        params["linehead_end"] = linehead_end
    if before is not None:
        params["before"] = before
    if after is not None:
        params["after"] = after

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/lines", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA 行文擷取失敗: {str(e)}")
