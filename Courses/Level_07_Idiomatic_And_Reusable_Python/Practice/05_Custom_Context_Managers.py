# Independent task: custom context managers
#
# Implement session(events) using contextmanager: append "enter" on entry, yield "active", and
# append "exit" in finally on every exit. Preserve exceptions raised by the body. Use it once
# successfully, appending its yielded value to events. Use it a second time with a deliberate
# ValueError in the body, catch that error outside the with, and append "caught". Print the
# final event list. Cleanup must occur before caught.
#
# Expected output:
#
# ['enter', 'active', 'exit', 'enter', 'exit', 'caught']

