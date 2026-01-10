import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_work_info(
    work: Annotated[str, Field(description="Scripture ID, e.g. 'T1501'")],
) -> dict:
    """
    Get CBETA scripture detailed information by work ID.
    
    Returns comprehensive scripture metadata:
    - work: scripture ID
    - title: scripture title
    - byline: author/translator info
    - creators: contributors
    - category: CBETA category
    - orig_category: original category
    - time_dynasty: dynasty
    - time_from/to: year range
    - cjk_chars: Chinese character count
    - en_words: English/Pali word count
    - file: file code
    - juan_start: starting fascicle
    - places: location list with coordinates
    """
    url = "https://api.cbetaonline.cn/works"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(url, params={"work": work})
            resp.raise_for_status()
            data = resp.json()

        if data.get("num_found", 0) == 0:
            return error_response("Scripture not found")

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
        return error_response(f"Failed to get scripture info: {str(e)}")
    except Exception as e:
        return error_response(f"Error: {str(e)}")
