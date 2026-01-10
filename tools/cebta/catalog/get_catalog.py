import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_catalog(
    q: Annotated[str, Field(description="查詢節點編號，如 'root'、'CBETA'、'orig-T'、'CBETA.001'")],
) -> dict:
    """
    📘 CBETA 佛典目錄結構查詢工具
    
    查詢 CBETA Online 提供的佛典目錄結構資料，可用於取得特定藏經分類、原書結構、或進一步展開經文節點。
    
    🔧 支援的查詢類型（q 參數）：
    - "root"：取得所有頂層目錄節點
    - "CBETA"：取得 CBETA 的部類目錄（阿含部、般若部、法華部等）
    - "orig"：取得所有原始藏經分類
    - "orig-T"：取得《大正藏》的原書結構目錄
    - "CBETA.001"：取得某一部類下的細節目錄
    
    📥 請求範例：
    - q: "root" → 取得頂層目錄
    - q: "CBETA" → 取得 CBETA 部類目錄
    - q: "CBETA.001" → 取得阿含部類下的佛典列表
    
    📤 回應範例：
    {
        "num_found": 21,
        "results": [
            {
                "n": "CBETA.001",
                "label": "01 阿含部類 T01-02,25,33 etc."
            },
            {
                "n": "CBETA.002",
                "label": "02 本緣部類 T03-04 etc."
            }
        ]
    }
    
    🔁 子節點查詢方式：
    可根據任一回傳項目的 `n` 字段進一步查詢下層：
    - 查詢 CBETA.001 的下層：q="CBETA.001"
    - 查詢大般若經內容：q="CBETA.003.001"
    
    ⚠️ 注意：若 node_type 為 'alt'，代表該節點未直接收錄全文，可透過對應藏經節點查詢。
    """
    url = "https://api.cbetaonline.cn/catalog_entry"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params={"q": q})
            response.raise_for_status()
            return success_response(response.json())
    except httpx.HTTPError as e:
        return error_response(f"HTTP 錯誤: {str(e)}")
    except Exception as e:
        return error_response(f"發生錯誤: {str(e)}")
