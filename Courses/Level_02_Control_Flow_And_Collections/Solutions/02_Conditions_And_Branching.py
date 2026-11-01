subtotal = 1200
if subtotal >= 1000:
    shipping = 0
else:
    shipping = 80
total = subtotal + shipping
print(f"Shipping: PHP {shipping}")
print(f"Total: PHP {total}")
