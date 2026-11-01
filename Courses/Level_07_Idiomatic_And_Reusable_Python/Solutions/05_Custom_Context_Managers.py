from contextlib import contextmanager

@contextmanager
def session(events):
    events.append("enter")
    try:
        yield "active"
    finally:
        events.append("exit")

events = []
with session(events) as state:
    events.append(state)
try:
    with session(events):
        raise ValueError("demonstration")
except ValueError:
    events.append("caught")
print(events)
