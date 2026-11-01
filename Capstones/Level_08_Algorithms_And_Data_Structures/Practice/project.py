# Independent task: Document search index with measured comparisons
#
# Implement tokenize(text), build_index(documents), scan_search(documents, query), and
# indexed_search(index, query). Use unique normalized query terms and return alphabetically
# sorted matching IDs. Missing terms and blank queries return []. Preserve source documents.
#
# Use documents D1: "python files", D2: "python async", and D3: "files storage". Demonstrate
# queries files and python files, confirming both variants agree. Benchmark each query method
# over a repeated workload for five trials and print actual median durations in nanoseconds;
# report index-construction duration separately. Demonstrate empty documents, blank queries, and
# missing-term queries, confirming that both variants return [] for each.
#
# Expected search lines:
#
# files: ['D1', 'D3']
# python files: ['D1']
#
# The remaining timing lines must contain measured nonnegative durations rather than fixed
# expected values.

