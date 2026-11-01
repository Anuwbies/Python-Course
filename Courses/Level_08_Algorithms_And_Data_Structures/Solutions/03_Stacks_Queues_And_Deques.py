def balanced_parentheses(text):
    stack = []
    for character in text:
        if character == "(":
            stack.append(character)
        elif character == ")":
            if not stack:
                return False
            stack.pop()
    return not stack

for text in ["(a(b)c)", ")(", ""]:
    print(balanced_parentheses(text))
