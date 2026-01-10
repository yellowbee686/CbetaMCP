import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_juan_html(
    work: Annotated[str, Field(description="佛典編號，如 'T0001'、'T1501'")],
    juan: Annotated[int, Field(description="卷號，從 1 開始")],
    work_info: Annotated[int, Field(description="是否回傳佛典資訊：0=否，1=是")] = 0,
    toc: Annotated[int, Field(description="是否回傳目次：0=否，1=是")] = 0,
) -> dict:
    """
    📘 CBETA 卷 HTML 內容抓取工具
    
    通過 CBETA API 抓取指定佛典的指定卷（juan）HTML 內容，
    可選是否同時返回「佛典資訊」與「目次」內容。
    
    📥 請求範例：
    - work: "T0001", juan: 1 → 長阿含經第1卷
    - work: "T0001", juan: 1, work_info: 1, toc: 1 → 同時返回佛典資訊與目次
    
    📤 回應範例：
    {
        "num_found": 1,
        "results": [
            {
                "juan": 1,
                "html": "<div id='body'>如是我聞。一時佛在...</div>"
            }
        ],
        "work_info": {
            "title": "長阿含經",
            "byline": "後秦 佛陀耶舍共竺佛念譯"
        },
        "toc": {
            "mulu": [...],
            "juan": [...]
        }
    }
    
    🏷️ 返回字段說明：
    - results[].juan: 卷號
    - results[].html: 該卷的 HTML 內容（含標記）
    - work_info: 佛典資訊（當 work_info=1 時返回）
    - toc: 目次結構（當 toc=1 時返回）
    
    🔧 用途：可用於閱讀器前端渲染、段落分析、結構轉換等。
    """
    try:
        url = "https://api.cbetaonline.cn/juans"
        params = {"work": work, "juan": juan, "work_info": work_info, "toc": toc}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA API 請求失敗: {str(e)}")
