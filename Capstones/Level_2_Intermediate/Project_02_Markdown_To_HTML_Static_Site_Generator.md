# Capstone Project 2.2: Markdown-to-HTML Static Site Generator

## 📌 Project Overview
Build a custom, lightweight **Static Site Generator (SSG)** in Python. The tool walks a source content directory containing Markdown files with YAML frontmatter, parses and converts markdown syntax into semantic HTML, injects content into reusable HTML layout templates, and renders the static build artifact into an output folder.

---

## 🎯 Learning Objectives
- **Generators & Iterators**: Stream and process large markdown documents line-by-line using `yield` and `yield from` to maintain $O(1)$ memory.
- **Context Managers**: Create custom context managers for temporary staging directories, file locks, and clean rollbacks on build errors.
- **Custom Decorators**: Implement pipeline transformation filters and build performance profilers.
- **Abstract Classes & Polymorphism**: Create abstract `BaseRenderer` and concrete renderers (HTML, Minified HTML, RSS Feed).
- **Comprehensive Unit Testing**: Test parser edge cases (nested lists, code blocks, escaped characters) using `pytest`.

---

## 🏗️ System Architecture

```text
               +----------------------------------+
               |        Static Site Builder       |
               +----------------------------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
+---------------+       +---------------+       +---------------+
|   SSG Context |       |  AST / Parser |       | BaseRenderer  |
|    Manager    |       |   Pipeline    |       |  (Abstract)   |
+---------------+       +---------------+       +---------------+
| - build_dir   |       | - frontmatter |       | + render()    |
| - temp_stage  |       | - headings    |       | + apply_layout|
| + __enter__() |       | - codeblocks  |       +-------+-------+
| + __exit__()  |       | - paragraphs  |               |
+---------------+       +---------------+       +-------+-------+
                                                |               |
                                        +---------------+ +---------------+
                                        | HTMLRenderer  | |  RSSRenderer  |
                                        +---------------+ +---------------+
```

---

## 📋 Functional Requirements

### 1. Frontmatter & Content Separation
Markdown files may contain YAML-like metadata headers:
```markdown
---
title: My First Article
date: 2026-08-18
tags: python, intermediate, ssg
---

# Hello World
This is **bold** text and *italic* text.
```
Your generator must extract metadata as a Python dictionary and feed the raw body to the Markdown parser pipeline.

### 2. Generator-Based Line & Block Parser
Implement a generator pipeline that processes markdown blocks:
- Headings (`# H1` -> `<h1>`, `## H2` -> `<h2>`, `### H3` -> `<h3>`)
- Inline formatting (`**bold**` -> `<strong>bold</strong>`, `*italic*` -> `<em>italic</em>`, `\`code\`` -> `<code>code</code>`)
- Code Blocks (Fenced ` ```python ... ``` ` -> `<pre><code class="language-python">...</code></pre>`)
- Unordered and Ordered Lists (`- item` -> `<ul><li>item</li></ul>`)
- Hyperlinks (`[Link Text](url)` -> `<a href="url">Link Text</a>`)

### 3. Custom Pipeline Decorators
- `@timing_benchmark`: Measures compile time per page and total site build duration.
- `@cache_build`: Skips regenerating HTML files whose source Markdown file has not modified since the last build timestamp.

### 4. Temporary Build Context Manager
```python
@contextmanager
def temporary_build_stage(target_dir: str):
    """
    Creates a temporary staging directory. If the entire build succeeds,
    atomically moves/renames the staged files into target_dir. If any
    exception occurs, removes the staging directory without affecting target_dir.
    """
```

---

## 📐 Phased Implementation Guide

### Phase 1: Generator Parsing Pipeline
```python
import re
from typing import Generator, Tuple, Dict, Any

def parse_frontmatter_stream(lines: Generator[str, None, None]) -> Tuple[Dict[str, Any], Generator[str, None, None]]:
    metadata = {}
    first_line = next(lines, "").strip()
    if first_line == "---":
        for line in lines:
            stripped = line.strip()
            if stripped == "---":
                break
            if ":" in stripped:
                key, val = stripped.split(":", 1)
                metadata[key.strip()] = val.strip()
    
    return metadata, lines
```

### Phase 2: Markdown AST Transformation
Convert inline regex matches into semantic HTML tags.

### Phase 3: Template Engine & Layout Injection
Replace placeholders like `{{ title }}`, `{{ content }}`, `{{ date }}` in layout template files.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Missing Frontmatter** | Markdown file without `---` header | Successfully processes document with empty metadata dict |
| **Nested Bold & Code** | `**Bold text with `code` inside**` | Produces `<strong>Bold text with <code>code</code> inside</strong>` |
| **Unclosed Code Fence**| Markdown file with opening ` ``` ` but no closing fence | Raises `MarkdownSyntaxError` with line number |
| **Build Failure Rollback**| Malformed template causes exception during page 4 of 10 | Target output folder remains in previous valid state |

---

## 🚀 Bonus Challenges
- **Sitemap & RSS Generator**: Automatically generate `sitemap.xml` and `feed.xml` from document frontmatter metadata.
- **Live Reload Server**: Use Python's built-in `http.server` to serve the generated site locally.
