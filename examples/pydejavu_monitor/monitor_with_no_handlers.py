from pydejavu.core.monitor import Monitor

specification = """
prop example: forall f . forall d . 
   write(f, d) ->
     (exists F . Exists s . 
       ((!close(f) S open(F, f, "w", s)) & (!delete(F) S create(F))))
"""

monitor = Monitor(specification)

events = [
    {"name": "create", "args": ["tmp"]},
    {"name": "open", "args": ["tmp", "f1", "w", "10"]},
    {"name": "write", "args": ["f1", "some text"]},
    {"name": "close", "args": ["f1"]},
    {"name": "delete", "args": ["tmp"]}
]

for e in events:
    monitor.verify(e)
monitor.end()