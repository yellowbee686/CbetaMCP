import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_similar_search(
    q: Annotated[str, Field(description="要搜尋的句子內容（不含標點），建議 6-50 字")],
    k: Annotated[int, Field(description="取回前 k 筆初始結果")] = 500,
    gain: Annotated[int, Field(description="比對演算法 match 加分")] = 2,
    penalty: Annotated[int, Field(description="比對演算法 miss 扣分")] = -1,
    score_min: Annotated[int, Field(description="最低匹配分數")] = 16,
    facet: Annotated[int, Field(description="是否回傳 facet：0=否，1=是")] = 0,
    cache: Annotated[int, Field(description="是否使用快取：1=是")] = 1,
) -> dict:
    """
    📘 CBETA 相似句搜尋工具
    
    使用 Manticore + Smith-Waterman 演算法實現句子相似搜尋。
    適合查找佛典中相似的經文段落、對照異譯本等場景。
    
    📥 請求範例：
    - q: "如是我聞一時佛在舍衛國祇樹給孤獨園" → 搜尋相似開經偈
    - q: "色即是空空即是色" → 搜尋般若心經相似段落
    - q: "已得善提捨不證" → 搜尋相似文句
    
    📤 回應範例：
    {
        "query_string": "如是我聞一時佛在舍衛國",
        "SQL": "SELECT ...",
        "time": 1.101,
        "num_found": 156,
        "cache_key": "...",
        "results": [
            {
                "work": "T0001",
                "title": "長阿含經",
                "juan": 1,
                "score": 24,
                "text": "如是我聞。一時佛在舍衛國祇樹給孤獨園..."
            }
        ]
    }
    
    🏷️ 返回字段說明：
    - num_found: 命中筆數
    - time: 執行時間（秒）
    - results[].score: 相似度分數
    - results[].text: 匹配的經文段落
    
    🔬 演算法說明：
    使用 Smith-Waterman 局部比對演算法，gain 為匹配加分，penalty 為錯配扣分。
    """
    try:
        params = {"q": q, "k": k, "gain": gain, "penalty": penalty, "score_min": score_min, "facet": facet, "cache": cache}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/similar", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA 相似搜尋失敗: {str(e)}")
