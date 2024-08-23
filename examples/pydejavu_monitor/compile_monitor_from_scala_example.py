from pydejavu.core.monitor import Monitor

dejavu = Monitor(i_bits=20, i_statistics=True)

# Compile the synthesized Scala monitor
compile_jar_path = dejavu.compile_monitor('/path/to/TraceMonitor.scala')

# Link the monitor to the compiled JAR file
dejavu.linkage_monitor(compile_jar_path)

y = 0
last_seen_q = False


# Define operational event handlers
@dejavu.operational("p")
def handle_p(arg_x: int):
    global y, last_seen_q
    x_lt_y = arg_x < y
    last_seen_q = False
    return ["p", arg_x, x_lt_y]


@dejavu.operational("q")
def handle_q(arg_y: int):
    global y, last_seen_q
    y = arg_y
    last_seen_q = True
    return ["q", arg_y]


for chunk in dejavu.read_bulk_events('/path/to/trace/file', chunk_size=10000):
    results = dejavu.verify.process_events(chunk)
    dejavu.logger.debug(f"Processed chunk of {len(chunk)} events")
    for result in results:
        dejavu.logger.debug(str(result))
