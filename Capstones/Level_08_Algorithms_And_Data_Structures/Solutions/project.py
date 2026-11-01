from statistics import median
from time import perf_counter_ns

def tokenize(text):
    return set(text.lower().split())

def build_index(documents):
    index = {}
    for doc_id, text in documents.items():
        for term in tokenize(text):
            index.setdefault(term, set()).add(doc_id)
    return index

def scan_search(documents, query):
    terms = tokenize(query)
    if not terms:
        return []
    return sorted(doc_id for doc_id, text in documents.items() if terms <= tokenize(text))

def indexed_search(index, query):
    terms = tokenize(query)
    if not terms:
        return []
    candidates = None
    for term in terms:
        ids = index.get(term, set())
        candidates = ids.copy() if candidates is None else candidates & ids
    return sorted(candidates)

def query_median(operation, repetitions=1000, trials=5):
    measurements = []
    for trial in range(trials):
        start = perf_counter_ns()
        for repetition in range(repetitions):
            operation()
        measurements.append(perf_counter_ns() - start)
    return int(median(measurements))

if __name__ == "__main__":
    documents = {"D1": "python files", "D2": "python async", "D3": "files storage"}
    start = perf_counter_ns()
    index = build_index(documents)
    build_ns = perf_counter_ns() - start
    for query in ["files", "python files"]:
        expected = scan_search(documents, query)
        assert indexed_search(index, query) == expected
        print(f"{query}: {expected}")
    for query in ["", "missing"]:
        assert scan_search(documents, query) == []
        assert indexed_search(index, query) == []
    assert scan_search({}, "files") == []
    assert indexed_search({}, "files") == []
    print(f"Index construction ns: {build_ns}")
    print(f"Scan query median ns: {query_median(lambda: scan_search(documents, 'python files'))}")
    print(f"Index query median ns: {query_median(lambda: indexed_search(index, 'python files'))}")
