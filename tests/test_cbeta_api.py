#!/usr/bin/env python3
"""
CBETA API Test Suite

Test all CBETA API endpoints to verify connectivity and correctness.
Run this script to diagnose API issues before debugging MCP tools.

Usage:
    python tests/test_cbeta_api.py
    python tests/test_cbeta_api.py --verbose
"""

import asyncio
import httpx
import time
import argparse
from dataclasses import dataclass
from typing import Any


BASE_URL = "https://api.cbetaonline.cn"
TIMEOUT = 30.0


@dataclass
class TestResult:
    """Test result container"""
    name: str
    endpoint: str
    success: bool
    duration_ms: float
    response_data: dict | None = None
    error: str | None = None
    

async def test_endpoint(
    client: httpx.AsyncClient,
    name: str,
    endpoint: str,
    params: dict[str, Any] | None = None,
) -> TestResult:
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    start = time.perf_counter()
    
    try:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        duration = (time.perf_counter() - start) * 1000
        
        return TestResult(
            name=name,
            endpoint=endpoint,
            success=True,
            duration_ms=duration,
            response_data=data,
        )
    except httpx.TimeoutException as e:
        duration = (time.perf_counter() - start) * 1000
        return TestResult(
            name=name,
            endpoint=endpoint,
            success=False,
            duration_ms=duration,
            error=f"Timeout: {str(e)}",
        )
    except httpx.HTTPStatusError as e:
        duration = (time.perf_counter() - start) * 1000
        return TestResult(
            name=name,
            endpoint=endpoint,
            success=False,
            duration_ms=duration,
            error=f"HTTP {e.response.status_code}: {str(e)}",
        )
    except Exception as e:
        duration = (time.perf_counter() - start) * 1000
        return TestResult(
            name=name,
            endpoint=endpoint,
            success=False,
            duration_ms=duration,
            error=str(e),
        )


async def run_all_tests(verbose: bool = False) -> list[TestResult]:
    """Run all API tests"""
    
    # Define all test cases: (name, endpoint, params)
    test_cases: list[tuple[str, str, dict[str, Any] | None]] = [
        # Health check (returns plain text, not JSON)
        # ("Health Check", "/health", None),
        
        # === Catalog Tools ===
        ("Catalog - Root", "/catalog_entry", {"q": "root"}),
        ("Catalog - CBETA", "/catalog_entry", {"q": "CBETA"}),
        ("Catalog - Ahan Section", "/catalog_entry", {"q": "CBETA.001"}),
        
        # === Works/Translator Search ===
        ("Works - Search by creator (安)", "/works", {"creator": "安"}),
        ("Works - Search by creator (竺)", "/works", {"creator": "竺"}),
        ("Works - Search by creator (玄奘)", "/works", {"creator": "玄奘"}),
        ("Works - Search by creator_id (A000294)", "/works", {"creator_id": "A000294"}),
        ("Works - Search by work ID (T0001)", "/works", {"work": "T0001"}),
        ("Works - Search by canon+vol (T01)", "/works", {"canon": "T", "vol": "T01"}),
        
        # === Dynasty Search ===
        ("Works - Search by dynasty (唐)", "/works", {"dynasty": "唐"}),
        ("Works - Search by time_from (600-700)", "/works", {"time_from": 600, "time_to": 700}),
        
        # === Fulltext Search ===
        ("Search - Fulltext (法鼓)", "/search", {"q": "法鼓", "rows": 5}),
        ("Search - Fulltext (般若)", "/search", {"q": "般若", "rows": 5}),
        
        # === Extended Search ===
        ("Search - Extended (AND)", "/search/extended", {"q": "般若 AND 波羅蜜", "rows": 5}),
        
        # === Title Search ===
        ("Search - Title (阿含)", "/search/title", {"q": "阿含", "rows": 5}),
        
        # === Work Content ===
        ("TOC - Get (T0001)", "/works/toc", {"work": "T0001"}),
        ("Juan - Get HTML (T0001 juan 1)", "/juans/goto", {"work": "T0001", "juan": 1}),
        ("Lines - Get (T0001)", "/lines", {"linehead": "T01n0001_p0001a01", "count": 5}),
        
        # === Other Search ===
        ("Search - Notes (校勘)", "/search/notes", {"q": "校勘", "rows": 5}),
        ("Search - SC (auto convert)", "/search/sc", {"q": "佛", "rows": 5}),
        ("Search - Facet Canon", "/search/facet/canon", {"q": "法鼓"}),
        ("Search - Facet Category", "/search/facet/category", {"q": "法鼓"}),
        ("Search - Facet Dynasty", "/search/facet/dynasty", {"q": "法鼓"}),
        ("Search - Synonym", "/search/synonym", {"q": "佛陀"}),
    ]
    
    results: list[TestResult] = []
    
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        print(f"\n{'='*60}")
        print("CBETA API Test Suite")
        print(f"Base URL: {BASE_URL}")
        print(f"Timeout: {TIMEOUT}s")
        print(f"{'='*60}\n")
        
        for name, endpoint, params in test_cases:
            result = await test_endpoint(client, name, endpoint, params)
            results.append(result)
            
            # Print result
            status = "✅" if result.success else "❌"
            print(f"{status} {result.name}")
            print(f"   Endpoint: {endpoint}")
            if params:
                print(f"   Params: {params}")
            print(f"   Duration: {result.duration_ms:.0f}ms")
            
            if result.error:
                print(f"   Error: {result.error}")
            elif verbose and result.response_data:
                # Show brief response info
                data = result.response_data
                if "num_found" in data:
                    print(f"   Results: {data.get('num_found', 0)} found")
                elif "results" in data:
                    print(f"   Results: {len(data.get('results', []))} items")
                elif "status" in data:
                    print(f"   Status: {data.get('status')}")
            
            print()
    
    return results


def print_summary(results: list[TestResult]) -> None:
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
                print(f"  - {r.name}: {r.error}")
    
    print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Test CBETA API endpoints")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show response details")
    args = parser.parse_args()
    
    results = await run_all_tests(verbose=args.verbose)
    print_summary(results)
    
    # Exit with error code if any test failed
    if any(not r.success for r in results):
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
