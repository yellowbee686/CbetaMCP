import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def synonym_search(
    q: Annotated[str, Field(description="查詢關鍵詞，如 '文殊師利'、'觀世音'")],
) -> dict:
    """
    📘 CBETA 近義詞搜索工具
    
    輸入關鍵詞，返回與該關鍵詞相關的近義詞列表。
    可用於文本理解、智能問答、佛典對照等場景。
    
    📥 請求範例：
    - q: "文殊師利" → 搜尋文殊師利的近義詞
    - q: "觀世音" → 搜尋觀世音的近義詞
    - q: "般若" → 搜尋般若的近義詞
    
    📤 回應範例：
    {
        "time": 0.001340973,
        "num_found": 9,
        "results": [
            "滿殊尸利",
            "曼殊室利",
            "妙德",
            "妙首",
            "妙吉祥",
            "文殊",
            "妙吉祥菩薩",
            "妙音",
            "曼殊"
        ]
    }
    
    🏷️ 返回字段說明：
    - time: 查詢耗時（秒）
    - num_found: 找到的近義詞數量
    - results: 近義詞列表
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/synonym", params={"q": q})
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"近義詞搜索失敗: {str(e)}")
