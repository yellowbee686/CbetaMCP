# CbetaMCP Development Guide

> CBETA Buddhist Scripture MCP Server - Development Documentation

---

## 1. Project Overview

### 1.1 Purpose

CbetaMCP is an MCP (Model Context Protocol) server that provides access to CBETA (Chinese Buddhist Electronic Text Association) APIs. It enables LLM agents to search, browse, and retrieve Buddhist scripture content.

### 1.2 Architecture

```
CbetaMCP/
├── main.py                 # FastAPI + FastMCP server entry point
├── requirements.txt        # Python dependencies
├── tools/                  # Tool modules (auto-discovered)
│   └── cebta/
│       ├── search/         # Fulltext search tools (10 tools)
│       ├── catalog/        # Catalog/directory tools (5 tools)
│       └── work/           # Scripture content tools (5 tools)
├── DEV_DOC.md             # This documentation
└── readme.md              # User-facing README
```

### 1.3 Tech Stack

- **MCP Framework**: `fastmcp>=2.0.0` - Modern MCP server implementation
- **Web Framework**: `fastapi>=0.115.0` - ASGI web framework
- **HTTP Client**: `httpx>=0.28.0` - Async HTTP client for CBETA API calls
- **Server**: `uvicorn>=0.34.0` - ASGI server

---

## 2. Quick Start

### 2.1 Installation

```bash
cd mcp_servers/CbetaMCP
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2.2 Running the Server

```bash
# Foreground (development)
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server endpoints:
- **FastAPI**: `http://localhost:8000`
- **MCP SSE**: `http://localhost:8000/mcp/sse`

### 2.3 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_PORT` | `8000` | Server port |
| `APP_BASE_URL` | `http://localhost:8000` | Base URL for API |

---

## 3. Tool Development Guide

### 3.1 Tool Structure

Each tool is a Python file in `tools/cebta/<category>/` directory. Tools are auto-discovered and registered at startup.

### 3.2 File Naming Convention

**推荐按函数名命名文件**，而不是用序号：

| ❌ 不推荐 | ✅ 推荐 | 原因 |
|----------|--------|------|
| `tools_1.py` | `get_work_info.py` | 一目了然知道功能 |
| `tools_2.py` | `get_toc.py` | 更容易查找和维护 |

### 3.3 Tool Template (Recommended)

**关键：docstring 中包含示例是让 LLM 正确调用工具的最重要因素！**

```python
import httpx
from typing import Annotated
from pydantic import Field
from main import __mcp_server__, success_response, error_response


@__mcp_server__.tool
async def get_cbeta_work_info(
    work: Annotated[str, Field(description="佛典編號，如 'T1501'、'T0001'")],
) -> dict:
    """
    📘 CBETA 佛典資訊查詢工具
    
    根據佛典編號（work ID）取得該佛典的詳細資訊。
    
    📥 請求範例：
    - work: "T1501" → 菩薩戒本
    - work: "T0001" → 長阿含經
    
    📤 回應範例：
    {
        "work": "T1501",
        "title": "菩薩戒本",
        "byline": "彌勒菩薩說 唐 玄奘譯",
        "category": "律部類",
        "time_dynasty": "唐"
    }
    
    🏷️ 返回字段：
    - work: 佛典編號
    - title: 佛典題名
    - byline: 作譯者說明
    - category: 分類
    """
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get("https://api.cbetaonline.cn/works", params={"work": work})
            resp.raise_for_status()
            return success_response(resp.json())
    except Exception as e:
        return error_response(f"錯誤：{str(e)}")
```

### 3.4 MCP 协议中 LLM 如何理解工具

LLM 通过以下信息决定如何调用工具：

```
┌─────────────────────────────────────────────────────┐
│  MCP Tool Definition (发送给 LLM)                    │
├─────────────────────────────────────────────────────┤
│  name: "get_cbeta_work_info"          ← 函数名       │
│  description: "📘 CBETA 佛典..."      ← docstring   │
│  inputSchema: {                        ← 参数 schema │
│    "properties": {                                  │
│      "work": {                                      │
│        "type": "string",                            │
│        "description": "佛典編號，如 'T1501'"        │
│      }                                              │
│    }                                                │
│  }                                                  │
└─────────────────────────────────────────────────────┘
```

**docstring 的最佳实践**：

| 元素 | 重要性 | 说明 |
|------|--------|------|
| 📥 请求范例 | ⭐⭐⭐ | **最重要！** 让 LLM 知道参数格式 |
| 📤 响应范例 | ⭐⭐⭐ | 让 LLM 知道如何处理返回值 |
| 🏷️ 字段说明 | ⭐⭐ | 帮助理解领域术语 |
| 功能描述 | ⭐⭐ | 简洁说明工具用途 |
| emoji 分隔 | ⭐ | 增加可读性 |

**为什么示例很重要？**

对于 CBETA 这种领域特定的 API：
- LLM 不一定知道 `T1501` 是什么格式
- 看到示例后立即理解应该传什么参数
- 看到返回示例后知道如何展示结果给用户

### 3.6 Key Patterns

1. **Decorator**: Use `@__mcp_server__.tool` (no parentheses)
2. **Parameters**: Use `Annotated[Type, Field(description="含示例的描述")]` for LLM visibility
3. **Docstring**: 必须包含请求/响应示例，这是 LLM 理解工具的关键
4. **Async**: All tools should be async functions
5. **Timeout**: Always set `httpx.AsyncClient(timeout=...)` to avoid hanging
6. **Response**: Use `success_response(dict)` or `error_response(str)`
7. **File Naming**: Use function name as filename (e.g., `get_work_info.py`)

### 3.7 Response Helpers

```python
from main import success_response, error_response

# Success response
return success_response({"key": "value"})
# Returns: {"status": "success", "result": {"key": "value"}}

# Error response
return error_response("Something went wrong")
# Returns: {"status": "error", "message": "Something went wrong"}
```

---

## 4. Available Tools

### 4.1 Search Tools (`tools/cebta/search/`)

| Tool | File | Description |
|------|------|-------------|
| `cbeta_fulltext_search` | tools_1.py | General fulltext search |
| `extended_search` | tools_2.py | AND/OR/NOT/NEAR syntax search |
| `synonym_search` | tools_3.py | Find related terms/synonyms |
| `cbeta_search_sc` | tools_4.py | Simplified/Traditional auto-convert |
| `cbeta_facet_query` | tools_5.py | Multi-dimensional facet query |
| `cbeta_all_in_one` | tools_6.py | Search with KWIC and facets |
| `search_cbeta_notes` | tools_7.py | Search annotations/collations |
| `search_title` | tools_8.py | Search scripture titles |
| `cbeta_kwic_search` | tools_9.py | Keyword in context (single volume) |
| `cbeta_similar_search` | tools_10.py | Similarity search (Smith-Waterman) |

### 4.2 Catalog Tools (`tools/cebta/catalog/`)

| Tool | File | Description |
|------|------|-------------|
| `get_cbeta_catalog` | tools_1.py | Browse catalog structure |
| `search_cbeta_texts` | tools_2.py | Search by keyword or volume |
| `search_buddhist_canons_by_vol` | tools_3.py | Search by canon and volume range |
| `search_works_by_translator` | tools_4.py | Search by author/translator |
| `search_cbeta_by_dynasty` | tools_5.py | Search by dynasty or year range |

### 4.3 Work/Content Tools (`tools/cebta/work/`)

| Tool | File | Description |
|------|------|-------------|
| `get_cbeta_work_info` | tools_1.py | Get scripture metadata |
| `get_cbeta_toc` | tools_2.py | Get table of contents |
| `get_juan_html` | tools_3.py | Get fascicle HTML content |
| `cbeta_goto` | tools_4.py | Navigate to specific position |
| `get_cbeta_lines` | tools_5.py | Get specific text lines |

---

## 5. CBETA API Reference

### 5.1 Base URL
- Production: `https://api.cbetaonline.cn`

### 5.2 Common Endpoints

| Endpoint | Description |
|----------|-------------|
| `/search` | General fulltext search |
| `/search/extended` | Extended search with operators |
| `/search/synonym` | Synonym lookup |
| `/search/facet` | Faceted search |
| `/search/all_in_one` | Combined search with KWIC |
| `/search/notes` | Annotation search |
| `/search/title` | Title search |
| `/search/kwic` | KWIC for single volume |
| `/search/similar` | Similarity search |
| `/catalog_entry` | Catalog structure |
| `/toc` | Table of contents |
| `/works` | Scripture metadata |
| `/juans` | Fascicle content |
| `/juans/goto` | Position navigation |
| `/lines` | Line-level content |

### 5.3 Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | str | Search query |
| `rows` | int | Results per page (default: 20) |
| `start` | int | Offset for pagination |
| `work` | str | Scripture ID (e.g., T0001) |
| `juan` | int | Fascicle number |
| `canon` | str | Canon ID (T, X, J, etc.) |

---

## 6. Integration with Madrid Project

### 6.1 MCP Configuration

In `config/mcp_config.json`:
```json
{
  "mcpServers": {
    "cbeta": {
      "url": "http://localhost:8001/mcp/sse",
      "transport": "sse",
      "description": "CBETA Buddhist Scripture Search MCP Server"
    }
  }
}
```

### 6.2 Starting with Madrid App

```bash
# Terminal 1: Start MCP Server
./scripts/start_mcp_server.sh --bg

# Terminal 2: Start Madrid App
LOCAL_AGENT_MCP_ENABLED=true uv run streamlit run app.py
```

---

## 7. Development Guidelines

### 7.1 Adding New Tools

1. Create new file in appropriate category: `tools/cebta/<category>/tools_N.py`
2. Follow the tool template in section 3.2
3. Use descriptive function names matching the CBETA API endpoint
4. Include comprehensive docstring for LLM understanding
5. Test the tool imports: `python -c "from tools.cebta.<category>.tools_N import *"`

### 7.2 Error Handling

- Always wrap API calls in try/except
- Use `error_response()` for user-friendly error messages
- Set appropriate timeouts (20-30s for most calls)
- Log errors for debugging when needed

### 7.3 Testing

```bash
# Test all imports
python -c "from main import app, mcp; print(f'Tools: {len(mcp._tool_manager._tools)}')"

# Run server and test with curl
uvicorn main:app --port 8001 &
# Then test MCP SSE endpoint
```

### 7.4 Code Style

- Use English for code comments and docstrings
- Type hints required for all parameters
- Async/await for all I/O operations
- Follow PEP 8 conventions

---

## 8. Troubleshooting

### 8.1 Common Issues

| Issue | Solution |
|-------|----------|
| Import error on startup | Check tool file syntax, ensure all imports are correct |
| Tool not registered | Ensure decorator is `@__mcp_server__.tool` (no parentheses) |
| API timeout | Increase `timeout` in `httpx.AsyncClient()` |
| Connection refused | Check CBETA API status, network connectivity |

### 8.2 Debug Mode

```bash
# Enable verbose logging
DEBUG=1 python main.py
```

---

## 9. Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.2.0 | 2026-01 | Migrated from fastapi-mcp to fastmcp, refactored all tools |
| 0.1.0 | Initial | Original implementation with fastapi-mcp |

---

## 10. References

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [CBETA Online API](https://api.cbetaonline.cn)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
