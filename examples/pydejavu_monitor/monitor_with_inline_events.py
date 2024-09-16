from pydejavu.core.monitor import Monitor, event

specification = """
prop example: forall f . 
  !write(f, "false") & 
  (write(f, "true") ->
    (exists F . ((!close(f) S open(F, f, "w")) & (!delete(F) S create(F)))))
"""

monitor = Monitor(specification)

total_sizes: dict[str, int] = {}


@event("open")
def open(Folder: str, file: str, mode: str, size: int):
    global total_sizes
    if mode == "w":
        total_sizes[file] = size
    return ["open", Folder, file, mode]


@event("close")
def close(file: str):
    global total_sizes
    del total_sizes[file]
    return ["close", file]


@event("write")
def write(file: str, data: str):
    global total_sizes
    if file not in total_sizes:
        total_sizes[file] = 0
    data_len = len(data)
    # Check if there is enough free space
    ok = total_sizes[file] >= data_len
    if ok:
        # Decrease free space
        total_sizes[file] -= data_len
    return ["write", file, ok]


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
