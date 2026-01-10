import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_facet_query(
    q: Annotated[str, Field(description="查詢關鍵字，如 '法鼓'、'般若'")],
    f: Annotated[str, Field(description="指定 facet 類型：canon/category/dynasty/creator/work")] = "canon",
) -> dict:
    """
    📘 CBETA Facet 多維面向查詢工具
    
    查詢 CBETA Online 的 Facet 結構，可按 5 種維度統計搜尋結果分布。
    
    ✅ 支援的 Facet 類型（f 參數，必須指定）：
    - canon：藏經編號（T、X、J 等）
    - category：部類（阿含部、大乘經等）
    - dynasty：朝代（唐、宋等）
    - creator：作譯者
    - work：佛典編號
    
    📥 請求範例：
    - q: "法鼓", f: "canon" → 返回藏經分布
    - q: "般若", f: "dynasty" → 返回朝代分布
    - q: "法鼓", f: "category" → 返回部類分布
    
    📤 回應範例（f="canon"）：
    [
        {"canon": "T", "docs": 382, "hits": 569, "canon_name": "大正藏"},
        {"canon": "X", "docs": 272, "hits": 384, "canon_name": "新纂卍續藏"}
    ]
    
    🏷️ 返回字段說明：
    - canon/category/dynasty/creator/work: 分類值
    - docs: 符合條件的文獻數
    - hits: 關鍵詞命中次數
    """
    try:
        # API requires facet type in path, e.g., /search/facet/canon
        url = f"https://api.cbetaonline.cn/search/facet/{f}"

        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params={"q": q})
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA facet 查詢失敗: {str(e)}")
