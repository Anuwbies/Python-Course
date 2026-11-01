total = 0
while True:
    response = input().strip().lower()
    if response == "done":
        break
    total = total + int(response)
print(f"Total: PHP {total}")
