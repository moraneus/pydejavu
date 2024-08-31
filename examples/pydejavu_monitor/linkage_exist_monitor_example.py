from pydejavu.core.monitor import Monitor, event

monitor = Monitor(i_bits=20, i_statistics=True)

# Link the monitor directly to the pre-compiled JAR file
monitor.linkage_monitor('/path/to/TraceMonitor.jar')


y = 0
last_seen_q = False


# Define operational event handlers
@event("p")
def handle_p(arg_x: int):
    global y, last_seen_q
    x_lt_y = arg_x < y
    last_seen_q = False
    return ["p", arg_x, x_lt_y]


@event("q")
def handle_q(arg_y: int):
    global y, last_seen_q
    y = arg_y
    last_seen_q = True
    return ["q", arg_y]


for chunk in monitor.read_bulk_events_as_dict('/path/to/trace/file', chunk_size=10000):
    results = monitor.verify(chunk)
    monitor.logger.debug(f"Processed chunk of {len(chunk)} events")
    for result in results:
        monitor.logger.debug(str(result))

    monitor.end()
