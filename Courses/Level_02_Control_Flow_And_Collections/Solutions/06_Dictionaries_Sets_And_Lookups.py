categories = ["food", "travel", "food"]
counts = {}
unique = set()
for category in categories:
    counts[category] = counts.get(category, 0) + 1
    unique.add(category)
print(counts["food"])
print(counts["travel"])
print(len(unique))
