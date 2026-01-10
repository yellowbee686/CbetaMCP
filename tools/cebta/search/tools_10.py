import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def cbeta_similar_search(
    q: Annotated[str, Field(description="Sentence to search (no punctuation, 6-50 characters recommended)")],
    k: Annotated[int, Field(description="Top k results from fuzzy search")] = 500,
    gain: Annotated[int, Field(description="Smith-Waterman match score gain")] = 2,
    penalty: Annotated[int, Field(description="Smith-Waterman mismatch penalty")] = -1,
    score_min: Annotated[int, Field(description="Minimum match score")] = 16,
    facet: Annotated[int, Field(description="Return facet: 0=no, 1=yes")] = 0,
    cache: Annotated[int, Field(description="Use cache: 1=yes, 0=no")] = 1,
) -> dict:
    """
    CBETA similar sentence search tool.
    
    Uses Manticore + Smith-Waterman algorithm for sentence similarity search.
    Good for finding similar passages across Buddhist scriptures.
    
    Returns:
    - query_string: search content
    - time: execution time in seconds
    - num_found: number of hits
    - results: matched data with scripture title, paragraph, sentence and alignment marks
    """
    try:
        params = {"q": q, "k": k, "gain": gain, "penalty": penalty, "score_min": score_min, "facet": facet, "cache": cache}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/search/similar", params=params)
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"CBETA similar search failed: {str(e)}")
