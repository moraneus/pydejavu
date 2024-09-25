from pydejavu.core.monitor import Monitor, event

specification = """
prop example: forall f . 
  !write(f, "false") & (write(f, "true") ->
    (exists F . ((!close(f) S open(F, f, "w")) & (!delete(F) S create(F)))))
"""
monitor = Monitor(specification)
total_sizes: dict[str, int] = {}


@event("open")
def open(F: str, f: str, m: str, s: int):
    global total_sizes
    if m == "w":
        total_sizes[f] = s
    return ["open", F, f, m]


@event("close")
def close(f: str):
    global total_sizes
    del total_sizes[f]
    return ["close", f]


@event("write")
def write(f: str, d: str):
    global total_sizes
    if f not in total_sizes:
        total_sizes[f] = 0
    data_len = len(d)
    ok = total_sizes[f] >= data_len
    if ok:
        total_sizes[f] -= data_len
    return ["write", f, ok]


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
