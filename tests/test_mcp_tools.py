#!/usr/bin/env python3
"""
MCP Tools Test Suite

Test all MCP tools by directly calling the underlying API functions.
This verifies that the tool implementations are correct.

Usage:
    cd mcp_servers/CbetaMCP
    python tests/test_mcp_tools.py
    python tests/test_mcp_tools.py --verbose
"""

import asyncio
import httpx
import time
import argparse
from dataclasses import dataclass
from typing import Any


BASE_URL = "https://api.cbetaonline.cn"
TIMEOUT = 30.0


def success_response(result: dict) -> dict:
    return {"status": "success", "result": result}


def error_response(message: str) -> dict:
    return {"status": "error", "message": message}


@dataclass
class ToolTestResult:
    """Test result container"""
    tool_name: str
    success: bool
    duration_ms: float
    result: dict | None = None
    error: str | None = None


# === Tool Implementation Functions (copied from tools for standalone testing) ===

async def test_get_cbeta_catalog(client: httpx.AsyncClient, q: str) -> dict:
    """Test get_cbeta_catalog tool"""
    url = f"{BASE_URL}/catalog_entry"
    resp = await client.get(url, params={"q": q})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_search_works_by_translator(
    client: httpx.AsyncClient,
    creator_id: str | None = None,
    creator: str | None = None,
    creator_name: str | None = None,
) -> dict:
    """Test search_works_by_translator tool"""
    url = f"{BASE_URL}/works"
    query_params = {}
    if creator_id:
        query_params["creator_id"] = creator_id
    elif creator:
        query_params["creator"] = creator
    elif creator_name:
        query_params["creator_name"] = creator_name
    else:
        return error_response("請至少提供一個搜尋參數")
    
    resp = await client.get(url, params=query_params)
    resp.raise_for_status()
    return success_response(resp.json())


async def test_search_cbeta_by_dynasty(
    client: httpx.AsyncClient,
    dynasty: str | None = None,
    time_from: int | None = None,
    time_to: int | None = None,
) -> dict:
    """Test search_cbeta_by_dynasty tool"""
    url = f"{BASE_URL}/works"
    query_params = {}
    if dynasty:
        query_params["dynasty"] = dynasty
    if time_from:
        query_params["time_from"] = time_from
    if time_to:
        query_params["time_to"] = time_to
    
    resp = await client.get(url, params=query_params)
    resp.raise_for_status()
    return success_response(resp.json())


async def test_search_buddhist_canons_by_vol(
    client: httpx.AsyncClient,
    canon: str,
    vol_from: str | None = None,
    vol_to: str | None = None,
) -> dict:
    """Test search_buddhist_canons_by_vol tool"""
    url = f"{BASE_URL}/works"
    query_params = {"canon": canon}
    if vol_from:
        query_params["vol_from"] = vol_from
    if vol_to:
        query_params["vol_to"] = vol_to
    
    resp = await client.get(url, params=query_params)
    resp.raise_for_status()
    return success_response(resp.json())


async def test_search_cbeta_texts(client: httpx.AsyncClient, q: str) -> dict:
    """Test search_cbeta_texts tool"""
    url = f"{BASE_URL}/search/toc"
    resp = await client.get(url, params={"q": q})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_fulltext_search(
    client: httpx.AsyncClient,
    q: str,
    rows: int = 20,
) -> dict:
    """Test cbeta_fulltext_search tool"""
    url = f"{BASE_URL}/search"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_extended_search(
    client: httpx.AsyncClient,
    q: str,
    rows: int = 20,
) -> dict:
    """Test extended_search tool"""
    url = f"{BASE_URL}/search/extended"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_search_title(client: httpx.AsyncClient, q: str, rows: int = 20) -> dict:
    """Test search_title tool"""
    url = f"{BASE_URL}/search/title"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_search_cbeta_notes(client: httpx.AsyncClient, q: str, rows: int = 20) -> dict:
    """Test search_cbeta_notes tool"""
    url = f"{BASE_URL}/search/notes"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_search_sc(client: httpx.AsyncClient, q: str, rows: int = 20) -> dict:
    """Test cbeta_search_sc tool"""
    url = f"{BASE_URL}/search/sc"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_facet_query(client: httpx.AsyncClient, q: str, f: str = "canon") -> dict:
    """Test cbeta_facet_query tool"""
    url = f"{BASE_URL}/search/facet/{f}"
    resp = await client.get(url, params={"q": q})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_synonym_search(client: httpx.AsyncClient, q: str) -> dict:
    """Test synonym_search tool"""
    url = f"{BASE_URL}/search/synonym"
    resp = await client.get(url, params={"q": q})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_all_in_one(client: httpx.AsyncClient, q: str, rows: int = 20) -> dict:
    """Test cbeta_all_in_one tool"""
    url = f"{BASE_URL}/search/all_in_one"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_kwic_search(client: httpx.AsyncClient, q: str, work: str) -> dict:
    """Test cbeta_kwic_search tool"""
    url = f"{BASE_URL}/search/kwic"
    resp = await client.get(url, params={"q": q, "work": work})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_similar_search(client: httpx.AsyncClient, q: str, rows: int = 20) -> dict:
    """Test cbeta_similar_search tool"""
    url = f"{BASE_URL}/search/similar"
    resp = await client.get(url, params={"q": q, "rows": rows})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_get_cbeta_work_info(client: httpx.AsyncClient, work: str) -> dict:
    """Test get_cbeta_work_info tool"""
    url = f"{BASE_URL}/works"
    resp = await client.get(url, params={"work": work})
    resp.raise_for_status()
    data = resp.json()
    if data.get("num_found", 0) == 0:
        return error_response(f"查無佛典：{work}")
    return success_response(data["results"][0])


async def test_get_cbeta_toc(client: httpx.AsyncClient, work: str) -> dict:
    """Test get_cbeta_toc tool"""
    url = f"{BASE_URL}/works/toc"
    resp = await client.get(url, params={"work": work})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_get_juan_html(client: httpx.AsyncClient, work: str, juan: int) -> dict:
    """Test get_juan_html tool"""
    url = f"{BASE_URL}/juans"
    resp = await client.get(url, params={"work": work, "juan": juan})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_cbeta_goto(client: httpx.AsyncClient, work: str, juan: int) -> dict:
    """Test cbeta_goto tool"""
    url = f"{BASE_URL}/juans/goto"
    resp = await client.get(url, params={"work": work, "juan": juan})
    resp.raise_for_status()
    return success_response(resp.json())


async def test_get_cbeta_lines(client: httpx.AsyncClient, linehead: str, count: int = 10) -> dict:
    """Test get_cbeta_lines tool"""
    url = f"{BASE_URL}/lines"
    resp = await client.get(url, params={"linehead": linehead, "count": count})
    resp.raise_for_status()
    return success_response(resp.json())


async def run_tool_test(
    client: httpx.AsyncClient,
    tool_name: str,
    test_func,
    **kwargs,
) -> ToolTestResult:
    """Run a single tool test"""
    start = time.perf_counter()
    
    try:
        result = await test_func(client, **kwargs)
        duration = (time.perf_counter() - start) * 1000
        
        if isinstance(result, dict) and result.get("status") == "error":
            return ToolTestResult(
                tool_name=tool_name,
                success=False,
                duration_ms=duration,
                result=result,
                error=result.get("message"),
            )
        
        return ToolTestResult(
            tool_name=tool_name,
            success=True,
            duration_ms=duration,
            result=result,
        )
    except Exception as e:
        duration = (time.perf_counter() - start) * 1000
        return ToolTestResult(
            tool_name=tool_name,
            success=False,
            duration_ms=duration,
            error=str(e),
        )


async def run_all_tests(verbose: bool = False) -> list[ToolTestResult]:
    """Run all MCP tool tests"""
    
    # Define test cases
    test_cases = [
        # === Catalog Tools ===
        ("get_cbeta_catalog (root)", test_get_cbeta_catalog, {"q": "root"}),
        ("get_cbeta_catalog (CBETA)", test_get_cbeta_catalog, {"q": "CBETA"}),
        ("search_works_by_translator (安)", test_search_works_by_translator, {"creator": "安"}),
        ("search_works_by_translator (玄奘)", test_search_works_by_translator, {"creator": "玄奘"}),
        ("search_works_by_translator (ID)", test_search_works_by_translator, {"creator_id": "A000294"}),
        ("search_cbeta_by_dynasty (唐)", test_search_cbeta_by_dynasty, {"dynasty": "唐"}),
        ("search_buddhist_canons_by_vol", test_search_buddhist_canons_by_vol, {"canon": "T", "vol_from": "T01", "vol_to": "T01"}),
        ("search_cbeta_texts", test_search_cbeta_texts, {"q": "般若"}),
        
        # === Search Tools ===
        ("cbeta_fulltext_search", test_cbeta_fulltext_search, {"q": "法鼓", "rows": 5}),
        ("extended_search", test_extended_search, {"q": "般若 AND 波羅蜜", "rows": 5}),
        ("search_title", test_search_title, {"q": "阿含", "rows": 5}),
        ("search_cbeta_notes", test_search_cbeta_notes, {"q": "校勘", "rows": 5}),
        ("cbeta_search_sc", test_cbeta_search_sc, {"q": "佛", "rows": 5}),
        ("cbeta_facet_query (canon)", test_cbeta_facet_query, {"q": "法鼓", "f": "canon"}),
        ("cbeta_facet_query (dynasty)", test_cbeta_facet_query, {"q": "法鼓", "f": "dynasty"}),
        ("synonym_search", test_synonym_search, {"q": "佛陀"}),
        ("cbeta_all_in_one", test_cbeta_all_in_one, {"q": "法鼓", "rows": 5}),
        ("cbeta_kwic_search", test_cbeta_kwic_search, {"q": "法鼓", "work": "T0270"}),
        ("cbeta_similar_search", test_cbeta_similar_search, {"q": "如是我聞一時佛在", "rows": 5}),
        
        # === Work Tools ===
        ("get_cbeta_work_info", test_get_cbeta_work_info, {"work": "T0001"}),
        ("get_cbeta_toc", test_get_cbeta_toc, {"work": "T0001"}),
        ("get_juan_html", test_get_juan_html, {"work": "T0001", "juan": 1}),
        ("cbeta_goto", test_cbeta_goto, {"work": "T0001", "juan": 1}),
        ("get_cbeta_lines", test_get_cbeta_lines, {"linehead": "T01n0001_p0001a01", "count": 5}),
    ]
    
    results: list[ToolTestResult] = []
    
    print(f"\n{'='*60}")
    print("MCP Tools Test Suite (Direct API Testing)")
    print(f"Base URL: {BASE_URL}")
    print(f"Total tools to test: {len(test_cases)}")
    print(f"{'='*60}\n")
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        for tool_name, test_func, kwargs in test_cases:
            result = await run_tool_test(client, tool_name, test_func, **kwargs)
            results.append(result)
            
            # Print result
            status = "✅" if result.success else "❌"
            print(f"{status} {result.tool_name}")
            print(f"   Kwargs: {kwargs}")
            print(f"   Duration: {result.duration_ms:.0f}ms")
            
            if result.error:
                print(f"   Error: {result.error}")
            elif verbose and result.result:
                data = result.result
                if isinstance(data, dict) and "result" in data:
                    inner = data["result"]
                    if isinstance(inner, dict):
                        if "num_found" in inner:
                            print(f"   Results: {inner.get('num_found', 0)} found")
                        elif "results" in inner:
                            print(f"   Results: {len(inner.get('results', []))} items")
                    elif isinstance(inner, list):
                        print(f"   Results: {len(inner)} items")
            
            print()
    
    return results


def print_summary(results: list[ToolTestResult]) -> None:
    """Print test summary"""
    total = len(results)
    passed = sum(1 for r in results if r.success)
    failed = total - passed
    
    avg_duration = sum(r.duration_ms for r in results) / total if total > 0 else 0
    
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    print(f"Total: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Avg Duration: {avg_duration:.0f}ms")
    
    if failed > 0:
        print(f"\nFailed Tests:")
        for r in results:
            if not r.success:
                print(f"  - {r.tool_name}: {r.error}")
    
    print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Test MCP tools directly")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show response details")
    args = parser.parse_args()
    
    results = await run_all_tests(verbose=args.verbose)
    print_summary(results)
    
    # Exit with error code if any test failed
    if any(not r.success for r in results):
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
