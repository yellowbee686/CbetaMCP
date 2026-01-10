import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_toc(
    work: Annotated[str, Field(description="佛典編號，如 'T0001'、'T1501'、'X0600'")],
) -> dict:
    """
    📘 CBETA 佛典目次查詢工具
    
    通過 CBETA Online API 獲取指定佛典的目次（Table of Contents）結構。
    
    📥 請求範例：
    - work: "T0001" → 長阿含經的目次
    - work: "T1501" → 菩薩戒本的目次
    
    📤 回應範例：
    {
        "num_found": 1,
        "results": [
            {
                "mulu": [
                    {
                        "title": "序",
                        "file": "T01n0001",
                        "juan": 1,
                        "lb": "0001a02",
                        "type": "序"
                    },
                    {
                        "title": "1 分",
                        "type": "分",
                        "n": 1,
                        "isFolder": true,
                        "children": [
                            {"title": "1 大本經", "type": "經", "n": 1}
                        ]
                    }
                ]
            }
        ]
    }
    
    🏷️ 返回字段說明：
    - mulu: 目次節點列表
    - title: 目次節點標題
    - file: 所在 XML 檔主檔名
    - juan: 所在卷號
    - lb: 頁、欄、行位置（如 "0001a02" = 第1頁a欄第2行）
    - type: 節點類型（序、分、經、品 等）
    - n: 節點序號
    - isFolder: 是否有子節點
    - children: 子目次節點
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get("https://api.cbetaonline.cn/toc", params={"work": work})
            response.raise_for_status()
            return success_response(response.json())
    except Exception as e:
        return error_response(f"取得 CBETA 目次失敗: {str(e)}")
