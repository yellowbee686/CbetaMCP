import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_facet_query(
    q: Annotated[str, Field(description="查詢關鍵字，如 '法鼓'、'般若'")],
    f: Annotated[str | None, Field(description="指定 facet 類型：canon/category/dynasty/creator/work，不指定則返回全部")] = None,
) -> dict:
    """
    📘 CBETA Facet 多維面向查詢工具
    
    查詢 CBETA Online 的 Facet 結構，可按 5 種維度統計搜尋結果分布。
    
    ✅ 支援的 Facet 類型（f 參數）：
    - canon：藏經編號（T、X、J 等）
    - category：部類（阿含部、大乘經等）
    - dynasty：朝代（唐、宋等）
    - creator：作譯者
    - work：佛典編號
    
    📥 請求範例：
    - q: "法鼓" → 返回全部 5 類 Facet
    - q: "法鼓", f: "canon" → 只返回藏經分布
    - q: "般若", f: "dynasty" → 只返回朝代分布
    
    📤 回應範例：
    {
        "canon": [
            {"value": "T", "count": 27},
            {"value": "X", "count": 15}
        ],
        "category": [
            {"value": "大乘經", "count": 15},
            {"value": "禪宗部類", "count": 12}
        ],
        "dynasty": [
            {"value": "唐", "count": 9},
            {"value": "宋", "count": 7}
        ],
        "creator": [
            {"value": "釋道宣", "count": 3}
        ],
        "work": [
            {"value": "T01n0001", "count": 2}
        ]
    }
    """
    try:
        base_url = "https://api.cbetaonline.cn/search/facet"
        url = f"{base_url}/{f}" if f else base_url

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params={"q": q})
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA facet 查詢失敗: {str(e)}")
