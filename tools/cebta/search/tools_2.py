import httpx
from typing import Annotated
from urllib.parse import quote
from pydantic import Field
from main import __mcp_server__, success_response, error_response

# 📘 CBETA Extended Search Tool
# Supports AND, OR, NOT, NEAR syntax for fulltext search.
# Query syntax:
# - AND: each word with quotes separated by space => `"法鼓" "聖嚴"`
# - OR: with | operator => `"波羅蜜" | "波羅密"`
# - NOT: with ! => `"迦葉" !"迦葉佛"`
# - NEAR: with NEAR/distance => `"法鼓" NEAR/7 "迦葉"`


@__mcp_server__.tool
async def extended_search(
    q: Annotated[str, Field(description="Query string with AND/OR/NOT/NEAR syntax")],
    start: Annotated[int, Field(description="Start position")] = 0,
    rows: Annotated[int, Field(description="Number of rows to return")] = 20,
) -> dict:
    """
    CBETA extended mode fulltext search tool.
    
    Supports AND, OR, NOT, NEAR syntax for advanced queries.
    Doc: https://api.cbetaonline.cn/search/extended
    """
    try:
        encoded_query = quote(q)
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(
                "https://api.cbetaonline.cn/search/extended",
                params={"q": encoded_query, "start": start, "rows": rows},
            )
            resp.raise_for_status()
            data = resp.json()

        total = data.get("total", 0)
        rows_data = [
            {
                "title": r.get("title", ""),
                "juan": r.get("juan", ""),
                "content": r.get("content", ""),
            }
            for r in data.get("results", [])
        ]
        return success_response({"total": total, "rows": rows_data})
    except Exception as e:
        return error_response(f"CBETA extended search failed: {str(e)}")
