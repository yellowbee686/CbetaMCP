import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_kwic_search(
    work: Annotated[str, Field(description="佛典編號，如 'T0001'、'X0600'")],
    juan: Annotated[int, Field(description="卷號")],
    q: Annotated[str, Field(description="查詢關鍵詞，可含 NEAR、排除詞等語法")],
    note: Annotated[int, Field(description="是否含夾注：0=不含，1=含")] = 1,
    mark: Annotated[int, Field(description="是否加 mark 標記：0=不加，1=加")] = 0,
    sort: Annotated[str, Field(description="排序：'f'=關鍵詞後排序，'b'=前排序，'location'=依出現位置")] = "f",
) -> dict:
    """
    📘 CBETA KWIC 單卷關鍵詞檢索工具
    
    提供 CBETA 的 KWIC（Keyword in Context）單卷前後文檢索功能，
    可支援 NEAR 查詢、排除詞、夾注開關與排序控制。
    
    📥 請求範例：
    - work: "T0001", juan: 1, q: "老子" → 搜尋長阿含經第1卷中的「老子」
    - work: "T0001", juan: 1, q: '"老子" NEAR/5 "道"' → NEAR 搜尋
    - work: "T0001", juan: 1, q: "老子", mark: 1 → 返回帶 mark 標記的結果
    
    📤 回應範例：
    {
        "num_found": 4,
        "time": 0.021964698,
        "results": [
            {
                "vol": "T36",
                "lb": "0002b03",
                "kwic": "...<mark>老子</mark>...<mark>道</mark>..."
            }
        ]
    }
    
    🏷️ 返回字段說明：
    - num_found: 命中結果數
    - time: 查詢耗時（秒）
    - results[].vol: 冊號
    - results[].lb: 行標位置（頁欄行）
    - results[].kwic: 前後文上下文（含關鍵詞）
    """
    try:
        params = {"work": work, "juan": juan, "q": q, "note": note, "mark": mark, "sort": sort}
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/kwic", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA KWIC 搜尋失敗: {str(e)}")
