from pydejavu.core.monitor import Monitor

specification = """
 prop example : forall x . forall y . ((p(x, "true") & @q(y)) -> P r(x, y))
 """

dejavu = Monitor(i_spec=specification, i_bits=20, i_statistics=True)
dejavu.init_monitor()

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
        dejavu.logger.debug(result)