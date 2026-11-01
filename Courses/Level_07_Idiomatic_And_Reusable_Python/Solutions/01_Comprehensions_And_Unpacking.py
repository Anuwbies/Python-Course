amounts = [0, 10, 20]
labels = [" FOOD ", "Travel", "food"]
doubled = [amount * 2 for amount in amounts if amount > 0]
unique = {label.strip().lower() for label in labels}
print(doubled)
print(sorted(unique))
print(amounts)
