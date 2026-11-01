# Level 8 capstone: Document search index with measured comparisons

**Prerequisites:** [all lessons in Level 8](../../Courses/Level_08_Algorithms_And_Data_Structures/README.md). **Submission:** `Practice/project.py`.

Build an inverted index mapping normalized terms to document IDs, and compare indexed queries with a full scan. Both variants must implement the same AND-query contract before their durations are compared.

Tokenization here is deliberately whitespace-based: text.lower().split() splits on runs of whitespace and preserves punctuation within a token. This is a small exact-token search model, not a complete natural-language search engine. Blank queries return no results, and repeated terms do not change the result.

Using the dictionary/set operations taught in Level 2, the index uses `mapping.setdefault(term, set())` to obtain an existing term set or store a newly created empty set. Set `<=` tests the subset relationship required by an AND query; `&` intersects candidates. These operations express matching terms without changing the source document strings.

Measure repeated query execution with perf_counter_ns and report medians, stating that index construction is excluded from these query-only timings. Also measure construction separately. Timing values depend on the machine; do not impose a fixed speedup or print invented measurements.

## Project task

Implement tokenize(text), build_index(documents), scan_search(documents, query), and indexed_search(index, query). Use unique normalized query terms and return alphabetically sorted matching IDs. Missing terms and blank queries return []. Preserve source documents.

Use documents `D1: "python files"`, `D2: "python async"`, and `D3: "files storage"`. Demonstrate queries files and python files, confirming both variants agree. Benchmark each query method over a repeated workload for five trials and print actual median durations in nanoseconds; report index-construction duration separately. Demonstrate empty documents, blank queries, and missing-term queries, confirming that both variants return [] for each.

Expected search lines:

```text
files: ['D1', 'D3']
python files: ['D1']
```

The remaining timing lines must contain measured nonnegative durations rather than fixed expected values.
