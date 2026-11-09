---
name: crawl4ai-skill
description: "Web crawling and scraping with LLM-optimized output. Supports DuckDuckGo search, site crawling, dynamic pages, and structured extraction. Free; no API key required."
version: 1.1.0
author: Lancelin
license: MIT-0
repository: https://github.com/lancelin111/crawl4ai-skill
homepage: https://github.com/lancelin111/crawl4ai-skill
pypi: crawl4ai-skill
issues: https://github.com/lancelin111/crawl4ai-skill/issues
tags:
  - web-scraping
  - web-crawling
  - crawler
  - scraper
  - spider
  - search
  - markdown
  - llm
  - token-optimization
  - duckduckgo
  - crawl
  - scrape
  - Web crawler
  - Crawl
  - Web Fetch
requires:
  bins:
    - crawl4ai-skill
---

# Crawl4AI Skill - Web Crawler & Scraper

**Web Crawling | Web Scraping | LLM-optimized output**

Free web crawler and scraper with search, full-site crawling, dynamic-page support, and LLM-optimized Markdown output.

## Core Functions | Core Features

- 🔍 **Web Search Web Search** - DuckDuckGo search, No, I don't think so. API key
- 🕷️ **Web Crawling** - Site crawler, spider, and sitemap discovery
- 📝 **Web Scraping Web Fetch** - Smart scraper, data extraction
- 📄 **LLM-Optimized Output** - Fit Markdown, Province Token 80%
- ⚡ **Dynamic Page Scraping** - JavaScript Render Page Crawling

---

## Quick Start | Quick Start

### Install | Installation

```bash
pip install crawl4ai-skill
```

### Web Search | Web Search

```bash
# Search the web with DuckDuckGo
crawl4ai-skill search "python web scraping"
```

### Web Scraping | Single Page Crawling

```bash
# Scrape a single web page
crawl4ai-skill crawl https://example.com
```

### Web Crawling | Full-site crawl

```bash
# Crawl entire website / spider
crawl4ai-skill crawl-site https://docs.python.org --max-pages 50
```

---

## Use scenes | Use Cases

### Scenario 1: Crawl a documentation site

```bash
# Crawl documentation site with spider
crawl4ai-skill crawl-site https://docs.fastapi.com --max-pages 100
```

**Crawler output:**
- ❌ Remove: Navigator Bar, Sidebar, Advertisement
- ✅ Reservation: Title, body, code block
- 📊 **Token：50,000 → 10,000（-80%）**

### Scene 2：Search + Scrape | Search+Crawl

```bash
# Search and scrape top results
crawl4ai-skill search-and-crawl "Vue 3 best practices" --crawl-top 3
```

### Scene 3：Dynamic Page Scraping | Dynamic Page Fetch

JavaScript Rendered page crawling (snowball, knowledge, etc.):

```bash
# Scrape JavaScript-heavy pages
crawl4ai-skill crawl https://xueqiu.com/S/BIDU --wait-until networkidle --delay 2
```

---

## Command reference | Commands

| Command Command | Annotations Description |
|------|------|
| `search <query>` | Web search Web Search |
| `crawl <url>` | Web scraping Single Page Crawling |
| `crawl-site <url>` | Crawl an entire site. |
| `search-and-crawl <query>` | Search + scrape Search and crawl |

### Common parameters | Common Options

```bash
# Web Search Search
--num-results 10          # Number of results

# Web Scraping Crawl
--format fit_markdown     # Output format
--output result.md        # Output file
--wait-until networkidle  # Wait strategy for dynamic pages
--delay 2                 # Additional wait time (seconds)
--wait-for ".selector"    # Wait for specific element

# Crawl a website
--max-pages 100          # Max pages to crawl
--max-depth 3            # Max crawl depth
```

---

## Output Format | Output Formats

### fit_markdown（Recommendations Recommended）

Smart extraction, savings 80% Token。Smart extraction, save 80% tokens.

```bash
crawl4ai-skill crawl https://example.com --format fit_markdown
```

### raw_markdown

Keep the complete structure.Preserve full structure.

```bash
crawl4ai-skill crawl https://example.com --format raw_markdown
```

---

## Why choose this crawler?

✅ **Free Crawler** - No API key is required; it works out of the box.
✅ **Smart Scraper** - Automatically extracts the main content.
✅ **Site Crawler** - Supports sitemaps and recursive crawling.
✅ **Dynamic Scraping** - Supports JavaScript-rendered pages.
✅ **Search Integration** - Includes DuckDuckGo search.

---

## Link | Links

- 📦 [PyPI](https://pypi.org/project/crawl4ai-skill/)
- 💻 [GitHub](https://github.com/lancelin111/crawl4ai-skill/)
- 🦞 [ClawHub](https://clawhub.com/skills/crawl4ai-skill)


## Mirror description (additional to this open warehouse)
- This document is a mirror of the upstream original; the supporting documentation was not distributed with the mirror, and the full original is available at the upstream warehouse/Bag.
- If supporting documents are cited for implementation skills, then the relative path is parsed from upstream.
