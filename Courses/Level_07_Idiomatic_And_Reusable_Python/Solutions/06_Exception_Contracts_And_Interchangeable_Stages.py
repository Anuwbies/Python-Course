class InvalidAmount(ValueError):
    """An invalid amount under this interface."""

def parse_amount(text):
    try:
        amount = int(text)
    except ValueError as error:
        raise InvalidAmount("Invalid amount text") from error
    if amount < 0:
        raise InvalidAmount("Amount cannot be negative")
    return amount

print(parse_amount("12"))
try:
    parse_amount("tea")
except InvalidAmount as error:
    print(type(error.__cause__).__name__)
