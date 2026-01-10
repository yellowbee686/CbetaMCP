import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def search_cbeta_texts(
    q: Annotated[str, Field(description="搜尋關鍵詞或藏經冊號，如 '阿含'、'T01'")],
) -> dict:
    """
    📘 CBETA 佛典經目搜尋工具
    
    根據關鍵詞或冊號搜尋 CBETA 佛典經目。
    
    🔍 搜尋情境：
    1. 關鍵詞搜尋：q="阿含" → 搜尋包含「阿含」的佛典
    2. 冊號搜尋：q="T01" → 搜尋大正藏第1冊的佛典
    
    📥 請求範例：
    - q: "阿含" → 搜尋阿含相關佛典
    - q: "般若" → 搜尋般若相關佛典
    - q: "T01" → 大正藏第1冊
    
    📤 回應範例：
    {
        "num_found": 46,
        "results": [
            {
                "type": "catalog",
                "n": "Cat-T.001",
                "label": "TB01 阿含部 T01~02 (1~151 經)"
            },
            {
                "type": "work",
                "n": "T0001",
                "label": "長阿含經"
            },
            {
                "type": "toc",
                "n": "T0001.001",
                "label": "序品 第一"
            }
        ]
    }
    
    🏷️ type 欄位說明：
    - catalog：部類目錄
    - work：經名層級（佛典標題）
    - toc：佛典內目次層級
    """
    # API path: /search/toc (not /toc)
    url = "https://api.cbetaonline.cn/search/toc"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params={"q": q})
            response.raise_for_status()
            return success_response(response.json())
    except httpx.HTTPError as e:
        return error_response(f"HTTP 錯誤: {str(e)}")
    except Exception as e:
        return error_response(f"發生錯誤: {str(e)}")
