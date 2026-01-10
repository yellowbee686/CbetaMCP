import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_work_info(
    work: Annotated[str, Field(description="佛典編號，如 'T1501'、'T0001'、'X0600'")],
) -> dict:
    """
    📘 CBETA 佛典資訊查詢工具
    
    根據佛典編號（work ID）取得該佛典的詳細資訊，包括標題、作譯者、朝代、分類、字數等。
    
    📥 請求範例：
    - work: "T1501" → 菩薩戒本
    - work: "T0001" → 長阿含經
    - work: "X0600" → 楞嚴經疏解蒙鈔
    
    📤 回應範例：
    {
        "work": "T1501",
        "title": "菩薩戒本",
        "byline": "彌勒菩薩說 唐 玄奘譯",
        "creators": "彌勒菩薩,玄奘",
        "category": "律部類",
        "time_dynasty": "唐",
        "time_from": 649,
        "time_to": 649,
        "cjk_chars": 7748,
        "places": [{"name": "大慈恩寺", "latitude": 34.219161, "longitude": 108.959356}]
    }
    
    🏷️ 返回字段說明：
    - work: 佛典編號
    - title: 佛典題名（經名）
    - byline: 作譯者說明
    - creators: 貢獻者列表
    - category: CBETA 分類
    - orig_category: 底本原始分類
    - time_dynasty: 朝代
    - time_from/to: 成立時間範圍（西元年）
    - cjk_chars: 中文字數
    - en_words: 英文/巴利單字數
    - file: 檔案代碼
    - juan_start: 起始卷
    - places: 翻譯地點（含經緯度）
    """
    url = "https://api.cbetaonline.cn/works"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params={"work": work})
            resp.raise_for_status()
            data = resp.json()

        if data.get("num_found", 0) == 0:
            return error_response(f"查無佛典：{work}")

        result = data["results"][0]
        return success_response({
            "work": result.get("work"),
            "title": result.get("title"),
            "byline": result.get("byline"),
            "creators": result.get("creators"),
            "category": result.get("category"),
            "orig_category": result.get("orig_category"),
            "time_dynasty": result.get("time_dynasty"),
            "time_from": result.get("time_from"),
            "time_to": result.get("time_to"),
            "cjk_chars": result.get("cjk_chars"),
            "en_words": result.get("en_words"),
            "file": result.get("file"),
            "juan_start": result.get("juan_start"),
            "places": result.get("places"),
        })
    except httpx.HTTPError as e:
        return error_response(f"取得佛典資料失敗：{str(e)}")
    except Exception as e:
        return error_response(f"錯誤：{str(e)}")
