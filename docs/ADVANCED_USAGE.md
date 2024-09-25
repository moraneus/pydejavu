# Advanced Usage

`PyDejaVu` is available both as a command-line tool and as a Python module that can be imported 
into your projects. 

## Python Module Usage
`PyDejaVu` can also be imported as a Python module into your scripts or 
projects for more flexible and integrated runtime verification.

### Step 1: Import the Library
To use `PyDejaVu` as a module, import the necessary classes and functions into your Python script:
```python
from pydejavu.core.monitor import Monitor, event
```

### Step 2: Define Your Specification

Start by defining the properties you want to monitor using a first-order logic specification. 
These properties describe the conditions or invariants that you expect to hold over the event streams.

```python
specification = """
 prop example : forall x . forall y . ((p(x, "true") & @q(y)) -> P r(x, y))
"""
```

### Step 3: Initialize the Monitor
Create an instance of the Monitor class, passing in your specification and other optional parameters. The Monitor constructor allows you to customize several aspects of the runtime verification process:

- `i_spec`: The specification string that defines the properties you want to monitor.
- `i_bits`: Defines the number of bits allocated for variables in the Binary Decision Diagrams (BDDs) 
used during the verification process. Increasing this value can improve precision but may impact performance. 
*(Default: 20)*
  - `i_mode`: An optional parameter that specifies the mode of operation. 
  This can be used to switch between different verification output modes:
  - `debug`: Enables comprehensive logging and diagnostic messages to help developers understand the 
  internal workings of the monitoring process, debug issues, and verify the correctness of the implementation. 
  This mode is especially useful during development and troubleshooting.
  - `profile`: Activates detailed performance profiling of the monitored properties, 
  recording metrics that can be analyzed to understand the efficiency and complexity of the property evaluations.
- `i_statistics`: A boolean flag that, if set to True, enables the collection of statistics during the 
verification process. (Default: False)
- `i_logging_level`: An optional parameter to define the logging level. 
If not provided, the default logging level is set to INFO.

Here is how you can initialize the Monitor:

```python
monitor = Monitor(i_spec=specification, i_bits=8)
```

#### Alternative Options for Monitor Initialization
While initializing a Monitor in `PyDejaVu` using a specification is common, you also have the flexibility to 
initialize the monitor using a pre-synthesized Scala monitor or a compiled monitor JAR file. 
These options are particularly useful when you already have a monitor synthesized or compiled outside the 
typical specification-based workflow.

##### Option 1: Initializing with a Synthesized Scala Monitor
In this option, you initialize the Monitor and then compile a Scala monitor file that has already been synthesized.
```python
# Initialize the Monitor with custom settings
monitor = Monitor(i_bits=20, i_statistics=False)

# Compile the synthesized Scala monitor
compile_jar_path = monitor.compile_monitor('/path/to/TraceMonitor.scala')

# Link the monitor to the compiled JAR file
monitor.linkage_monitor(compile_jar_path)
```

##### Option 2: Initializing with a Pre-Compiled Monitor JAR
If you already have a compiled monitor in the form of a JAR file, you can directly link this JAR file to the 
Monitor after initialization.
```python
# Initialize the Monitor with custom settings
monitor = Monitor(i_bits=20, i_statistics=False)

# Link the monitor directly to the pre-compiled JAR file
monitor.linkage_monitor('/path/to/TraceMonitor.jar')
```

### Step 4: Sharing Data Between Handlers
When handling events, you may need to share data between different event handlers. 
There are two primary ways to achieve this in `PyDejaVu`:

##### Global Variables:
 - You can use global variables to store and share data between handlers. 
This approach is straightforward and effective when the data to be shared is simple and doesn't need to 
persist beyond the lifetime of the program.
##### `PyDejaVu` Shared Variables API:
- `PyDejaVu` provides a built-in API for managing shared variables, which is particularly useful for more 
complex scenarios or when you want to maintain state across different parts of your program. 
- You can store and retrieve shared data using `monitor.set_shared("key", value)` and `monitor.get_shared("key", default_value)` 
respectively. This method ensures that your data is managed within the `PyDejaVu` framework, offering more 
control and avoiding potential issues with global variables.
- For example:
    ```python
    monitor.set_shared("last_seen_q", False)
    last_seen_q = monitor.get_shared("last_seen_q", False)
    ```
- Another type of shared variable function is the `monitor.last_eval("spec_name")` function which is a powerful feature 
that allows you to access the last evaluation result of a specified property. This can be especially useful 
within your event handlers when you need to consider the declarative verdict in your operational logic.
For example, within an handler function, you can check the last evaluation result of property "example" before 
making further decisions:
    ```python
  verdict = monitor.last_eval("example")
  if verdict:
  # Perform additional operations based on the last evaluation result
    pass

    ```


### Step 5: Define Operational Event Handlers
Define Python functions to handle the events specified in your logic. 
These handlers perform real-time operations on the events, such as arithmetic calculations, string manipulations, 
or state tracking. The handlers are decorated with the `@event("event_name")` decorator, 
linking them to specific events in your specification.
This definition is optional; if no handler is defined for a specific event, `PyDejaVu` will forward the 
event directly to DejaVu for evaluation. Without any handler definitions, PyDejaVu functions 
the same as `DejaVu` without the operational phase.

```python
y = 0
last_seen_q = False


# Define operational event handlers
@event("p") -> Tuple[str | bool | int, ...]
def handle_p(arg_x: int):
    global y, last_seen_q
    x_lt_y = arg_x < y
    last_seen_q = False
    return "p", arg_x, x_lt_y


@event("q")
def handle_q(arg_y: int) -> List[str | bool | int]:
    global y, last_seen_q
    y = arg_y
    last_seen_q = True
    return ["q", arg_y]
```
This code defines two operational event handlers, `handle_p` and `handle_q`, which are responsible for processing 
events named **"p"** and **"q"** respectively. 
These handlers are part of the two-phase runtime verification process facilitated by `PyDejaVu`, 
where events are processed in real-time using Pythonic operations, and the results can influence 
the monitoring and verification against a formal specification.

The `@event("p")` decorator is used to link the `handle_p` function to the event **"p"**. 
When an event named **"p"** is encountered in the event stream, `PyDejaVu` will automatically call the `handle_p` 
function to process it.  The `handle_p(arg_x: int)` function is designed to handle the **"p"** event. 
It takes an integer argument `arg_x` and uses the global variables `y` and `last_seen_q` to perform its operations.

Similarly, the `@event("q")` decorator links the `handle_q` function to the **"q"** event, 
ensuring that this function is called when a **"q"** event is encountered.

#### Handlers Returning Values
Handlers can return one of the following types:

- `Tuple[str | bool | int, ...]`: The first element is the event name, followed by event parameters 
(which can be strings, integers, or booleans).
- `List[str | int | bool]`: The first element is the event name, followed by event parameters 
(which can be strings, integers, or booleans).
- `None` or no return statement: In this case, `PyDejaVu` does not forward any event to the declarative phase, 
indicating only local computation was performed for later use.

### Step 6: Process Event Streams
You can now process streams of events using `PyDejaVu`. 
For instance, you can read events from a log file in chunks and pass them to the monitor for processing. 
The monitor will evaluate the events against your specifications.

```python
for chunk in monitor.read_bulk_events_as_dict('/path/to/trace/file', chunk_size=1000):
    results = monitor.verify.process_events(chunk)
    monitor.logger.debug(f"Processed chunk of {len(chunk)} events")
    for result in results:
        monitor.logger.debug(result)
```
You are not required to use the event iteration API to process events in `PyDejaVu`. 
Instead, you have the flexibility to process events individually or in batches using the following methods:

- Processing Multiple Events:
You can use the `monitor.verify.process_events(events)` or just `monitor.verify(events)` methods to process a batch (list) of events at once. 
This method is particularly useful when you have a list of events that need to be verified together.

- Processing a Single Event:
Alternatively, you can use the `monitor.verify.process_event(event)` or just `monitor.verify(event)` methods to process a single event whenever needed. 
This allows you to handle events as they occur in real-time or in specific scenarios where events are 
processed one at a time.

- Flexible Event Processing:  
`PyDejaVu` provides flexibility in how you process events by allowing you to use either `monitor.verify(events)` to process a list of events or `monitor.verify(event)` to process a single event. 
The method automatically handles the input based on whether it is a single event or a batch of events.


🔔 Each event can be either a dictionary of type `Dict[str, Any]` or a `string`.

If the event is a dictionary, it should include the following two keys:
- `name`: The name of the event.
- `args`: A list or dictionary containing the arguments associated with the event.
An example of a dictionary event is: `{'name': 'key', 'args': [arg1, arg2, ...]}`.

Alternatively, an event can be a string where the event name and arguments are separated by commas
without spaces. For example: `"event_name,arg1,arg2,..."`

When processing multiple events, you should provide a list of such dictionaries or 
strings (i.e., `List[[Dict[str, Any]]` or `List[str]`).
This structure ensures that each event is correctly recognized and processed by the `PyDejaVu` verification engine.

### Step 7: Finalize The Evaluation
Since DejaVu cannot detect when the evaluation ends because `PyDejaVu` forwards events asynchronously 
(the Python part works in an online manner with DejaVu), 
we must notify DejaVu at the end of the evaluation. 
Otherwise, the result file might not close properly. To ensure proper termination, 
call `monitor.end()` after processing all events.
Additionally, we have the `monitor.stat()` function that notifies `DejaVu` to execute its internal `end` function, 
which summarizes the results up to that point.
When calling to `monitor.end()` the `monitor.stat()` is called automatically. Below is an example of how the statistics looks like:
```bash
Processed 1000000 events

55392 errors detected!

==================
  Event Counts:
------------------
  p : 333432
  q : 333029
  r : 333539
==================
```

## Command-Line Interface (CLI) Usage

To use `PyDejaVu` from the command line, provide specific input files and parameters via command-line options:

### Command-Line Options

- `--bits`: Defines the number of bits allocated for variables in the Binary Decision Diagrams (BDDs) 
used during the verification process. Increasing this value can improve precision but may impact performance. 
*(Default: 20)*

- `--stats`: Toggles the collection of runtime statistics. Set to `true` to collect statistics, 
providing insights into performance and verification metrics, or `false` to disable. *(Default: false)*

- `--qtl`: Specifies the path to the QTL (Quantified Temporal Logic) file, which contains the temporal logic 
specifications for monitoring. This file follows the same format as required by DejaVu and is mandatory 
for execution.

- `--operational`: Specifies the path to the operational phase file, which includes dynamic event 
handlers to be used during runtime verification. These handlers are essential for processing events according 
to custom logic.

- `--trace`: Specifies the path to the trace file containing the event stream data for the monitor to analyze. 
This file is required to perform the verification process.

### Example
```bash
python3 -m pydejavu --bits 20 --stats true --qtl /path/to/spec.qtl --operational /path/to/events.pqtl --trace /path/to/trace.log
```

This command initializes the monitor with 20 bits, enables statistics, 
and uses the specified qtl, operational, and trace files for runtime verification.

## Trace File Format
The trace file used by `PyDejaVu` is identical to the one is used in `DejaVu`, 
and it should be in a comma-separated value (CSV) format,
similar to the format described in this [CSV file format guide](http://edoceo.com/utilitas/csv-file-format). 
The file defines a sequence of events that `PyDejaVu` will process during runtime verification.

### Example Trace File
Consider the following example of a trace file:
```csv
start,process,1
update,process,2.5
update,process,True
complete,process
```
This trace file describes four events with no leading spaces:
1. `start,process,1`
2. `update,process,2.5`
3. `update,process,True`
4. `complete,process`

Each line in the file corresponds to an event, where the first value is the event name, 
and the subsequent values are the arguments passed to that event.

### Handling of Booleans and Floats
`PyDejaVu` provides special handling for certain string values and numeric types to support flexible and 
accurate runtime verification.

#### Boolean Handling
Strings that represent boolean values, specifically "False", "false", "True", and "true", will be automatically 
interpreted as booleans by `PyDejaVu`. This means that when such strings are encountered in the trace file, 
they are treated as the boolean values False or True respectively.

#### Float Handling:
During the operational phase, `PyDejaVu` can handle floating-point numbers, 
allowing you to perform operations with decimal precision.
However, when these values are passed to the declarative phase 
(for example, in the logic specified in your properties), they will be automatically cast to integers. 
This casting ensures compatibility with the DejaVu formal verification process, which typically operates on integer values.

Example:
```csv
update,process,2.5
```
In the operational phase, this value can be handled as a float (2.5). 
When passed to the declarative phase, it will be cast to 2.