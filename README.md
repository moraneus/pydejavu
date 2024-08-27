# PyDejaVu

![PyPI](https://img.shields.io/pypi/v/PyDejaVu-RV)
![PyPI - Downloads](https://img.shields.io/pypi/dm/PyDejaVu-RV)
[![License: MIT](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/license/apache-2-0)

![pydejavu.png](https://raw.githubusercontent.com/moraneus/pydejavu/main/extra/images/pydejavu.jpg)

`PyDejaVu` is a Python library that wraps the original [DejaVu](https://github.com/havelund/dejavu/tree/master) binary, 
providing a bridge between Python and the 
Java-based DejaVu runtime verification tool. It is a powerful tool designed for two-phase 
Runtime Verification (RV) processing, similar to the [Tp-DejaVu](https://github.com/moraneus/TP-DejaVu) tool, 
combining the flexibility and expressiveness of 
Python with the rigorous, declarative monitoring capabilities of 
the DejaVu tool.

#### Two-Phase Runtime Verification

`PyDejaVu` operates in two distinct phases:

1. **Operational Runtime Verification (Phase 1):**
   - This phase is implemented in Python, allowing for any Pythonic operations on the events. 
   You can perform arithmetic, string manipulations, and Boolean logic, and leverage 
   Python's extensive data structures and objects for storing data and making complex calculations. 
   This flexibility enables `PyDejaVu` to handle a wide range of operational tasks during runtime, 
   offering users the ability to customize how events are processed and analyzed.

2. **Declarative Monitoring (Phase 2):**
   - The second phase is declarative and leverages the DejaVu tool to perform monitoring against a first-order 
   logic specification. This phase ensures that the runtime behavior conforms to the formal properties 
   defined in the specification. By integrating with DejaVu, `PyDejaVu` provides a robust framework for verifying 
   that the system adheres to specified safety and liveness properties, making it suitable for applications requiring 
   high levels of assurance.

#### Combining Python and DEJAVU

PyDejaVu bridges the gap between operational and declarative runtime verification, allowing users to define complex 
behaviors and verify them against formal specifications. Whether you're performing real-time analysis of event 
streams or ensuring that your system meets stringent correctness criteria, 
PyDejaVu offers a versatile solution that can be tailored to meet your needs.

With PyDejaVu, you can take advantage of Python's powerful capabilities in the first phase while relying 
on the declarative strength of DejaVu in the second phase, providing a comprehensive tool for runtime verification 
in a wide range of applications.

## Installation

### Source Code Installation

Installing the source code is a great option if you need more flexibility and control over the `PyDejaVu` project. 
Here are some reasons why you might choose this method:

- **Customization and Modification:** If you plan to modify the code to suit specific requirements or contribute to the project, installing the source code gives you direct access to all the files. This is ideal for developers who want to extend or alter the functionality of `PyDejaVu`.
- **Development and Debugging:** When working on new features or fixing bugs, having the source code installed locally allows you to test changes immediately. This setup is essential for contributors or developers actively working on the `PyDejaVu` project.
- **Learning and Exploration:** If you're interested in understanding how `PyDejaVu` works internally, studying the source code can be very educational. You can explore the implementation details, experiment with changes, and see how different components interact.



#### Prerequisites

Ensure that you have Python 3.8 or higher installed on your system. 
You will also need [Poetry](https://python-poetry.org/) for managing dependencies and packaging the project.

#### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/pydejavu.git
cd pydejavu
```

#### Step 2: Install Poetry
If you don't have Poetry installed, you can install it by following the instructions on the official [Poetry website](https://python-poetry.org/).

Alternatively, you can install it using the following command:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Ensure that Poetry is added to your PATH by running:
```bash
poetry --version
```

#### Step 3: Install Dependencies
With Poetry installed, you can now install the project dependencies. 

Run the following command in the root directory of the project:
```bash
poetry install
```
This command will create a virtual environment (if one doesn't already exist) and install all the 
dependencies specified in the pyproject.toml file.

#### Step 4: Activate the Virtual Environment
After installation, activate the virtual environment created by Poetry:
```bash
poetry shell
```
This will drop you into a shell with the virtual environment activated.

#### 🛠️ Troubleshooting
If you encounter issues during installation or while running the project, consider the following:

 - Ensure that your Python version meets the minimum requirement.
 - Check that Poetry is correctly installed and accessible from your command line. 
 - Verify that all dependencies are properly installed by running poetry show.

### Pip Installation 
For users who just need to use `PyDejaVu` without making any changes, `pip` provides a quick and hassle-free setup, 
allowing you to focus on using the tool rather than managing the codebase.
Installing `PyDejaVu` via `pip` is the simplest and most convenient method for most users. 
If you prefer to install `PyDejaVu` directly from PyPI using `pip`, you can do so with a single command.

#### Step 1: Install PyDejaVu

To install the latest version of `PyDejaVu` from PyPI, run the following command:
```bash
pip install PyDejaVu-RV
```
This command will automatically download and install `PyDejaVu` and all its dependencies.

If you need to upgrade `PyDejaVu` to the latest version, you can do so with:
```bash
pip install --upgrade py-dejavu
```


#### Step 2: Verify the Installation
After installation, you can verify that `PyDejaVu` has been installed correctly by checking the installed package list:
```bash
pip show pydejav
```

#### 🛠️ Troubleshooting
If you encounter any issues while installing or using `PyDejaVu` via pip, consider the following:

 - Ensure that your Python environment is correctly configured and that you have the necessary permissions to install packages. 
 - If you’re using a virtual environment, make sure it’s activated before running the pip install command.

### Docker Installation 

For those who want a streamlined setup without modifying their local environment, 
Docker offers a robust solution to run `PyDejaVu` in an isolated and consistent environment. 
By using Docker, you avoid dealing with dependencies and compatibility issues, as everything is pre-configured 
in a container. This approach is perfect for users who prefer not to alter their system settings or manage 
package installations manually. If you choose to use Docker, setting up and running `PyDejaVu` is 
straightforward and can be accomplished with just a few commands.

#### Prerequisites
Ensure Docker is installed on your system. You can download 
Docker from [here](https://docs.docker.com/engine/install/).

#### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/pydejavu.git
cd pydejavu
```

#### Step 2: Build the Docker Image

Build the Docker image using the provided Dockerfile:

```bash
docker build -t pydejavu .
```
This command builds a Docker image named "pydejavu".
When this Dockerfile is built, it creates a Docker image that sets up a complete 
environment for running `PyDejaVu`. The build process installs necessary system dependencies, 
including Java and Scala, configures Python with Poetry for dependency management, and installs 
`PyDejaVu` along with its dependencies. 
Additionally, it runs a linter and tests to ensure that everything is properly configured and working. 
The result is a ready-to-use Docker image that contains all the tools and libraries needed 
to run `PyDejaVu` seamlessly, providing a consistent and reproducible environment across different systems.

#### Step 4: Run the Docker Container
Run the Docker container using the image you just built:
```bash
docker run -it pydejavu
```
This command starts an interactive session inside the Docker container, 
where `PyDejaVu` is set up and ready to use.

#### Step 4: Operate PyDejaVu
Inside the Docker container, you can run `PyDejaVu` commands as needed. For example, to start monitoring:
```bash
python -m pydejavu <your-arguments>
```
Replace <your-arguments> with the specific arguments for your use case.


## Trace File Format
The trace file used by `PyDejaVu` should be in a comma-separated value (CSV) format, 
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
1. `start(process, 1)`
2. `update(process, 2.5)`
3. `update(process, True)`
4. `complete(process)`

Each line in the file corresponds to an event, where the first value is the event name, 
and the subsequent values are the arguments passed to that event.

### Special Keywords in Trace Files
In addition to regular event lines, the trace file format supports special keywords that signal specific 
actions to `PyDejaVu`. These keywords help manage the runtime verification process, 
particularly when handling online monitoring.

#### `#end#`:
- **Purpose**: Notifies `DejaVu` to execute its end function, which summarizes the results up to that point.
- **Usage**: This keyword is essential because `PyDejaVu` operates as an online monitoring tool with respect to DejaVu, 
where events are processed in real-time. 
Since `DejaVu` cannot inherently know when the event trace will end, 
the `#end#` keyword provides a clear signal to summarize and conclude the verification process.
- **Example**:
    ```csv
      start,process,1
      update,process,2.5
      #end#
    ```
- **Result**: After encountering #end#, DejaVu will summarize the results of the verification process up to this point.
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
  
#### `#init#`

- **Purpose**: Set all properties' last evaluation values to False.
- **Usage**: This keyword is typically used once at the beginning of the trace to initialize all properties to 
a `False` evaluation state. `PyDejaVu` automatically inserts this at the start of processing to 
ensure a consistent initial state for all properties. 
However, users can manually include `#init#` in the trace file if they wish to reset the properties' 
evaluation states to `False` at any point during the trace.
Doing so will not affect the DejaVu BDDs summaries or the error statistics, and the monitoring will 
continue from the last processed event.


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
This casting ensures compatibility with the formal verification process, which typically operates on integer values.

Example:
```csv
update,process,2.5
```
In the operational phase, this value can be handled as a float (2.5). 
When passed to the declarative phase, it will be cast to 2.

## Usage

`PyDejaVu` is a versatile tool that bridges Python's operational capabilities with the rigorous, 
declarative runtime verification offered by the DEJAVU tool. 
It can be used for two-phase Runtime Verification (RV) processing, 
allowing you to monitor properties of event streams using both Python and DEJAVU's first-order logic specifications.
`PyDejaVu` is available both as a command-line tool and as a Python module that can be imported into your projects.


### Command-Line Interface (CLI) Usage

To use `PyDejaVu` from the command line, provide specific input files and parameters via command-line options:

#### Command-Line Options

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

#### Example
```bash
python3 -m pydejavu --bits 20 --stats true --qtl /path/to/spec.qtl --pqtl /path/to/events.pqtl --trace /path/to/trace.log
```

This command initializes the monitor with 20 bits, enables statistics, 
and uses the specified QTL, PQTL, and trace files for runtime verification.


### Python Module Usage
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
- 
Here is how you can initialize the Monitor:

```python
monitor = Monitor(i_spec=specification, i_bits=8)
monitor.init_monitor()
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
the same as DejaVu without the operational phase.

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
You can use the `monitor.verify.process_events(events)` method to process a batch (list) of events at once. 
This method is particularly useful when you have a list of events that need to be verified together.

- Processing a Single Event:
Alternatively, you can use the `monitor.verify.process_event(event)` method to process a single event whenever needed. 
This allows you to handle events as they occur in real-time or in specific scenarios where events are 
processed one at a time.

- Flexible Event Processing:  
`PyDejaVu` provides flexibility in how you process events by allowing you to use either `monitor.verify(events)` to process a list of events or `monitor.verify(event)` to process a single event. The method automatically handles the input based on whether it is a single event or a batch of events.


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
call `monitor.verify.end_eval()` after processing all events.


## Examples
You can find comprehensive examples of monitors in the [examples](examples%2Fpydejavu_monitor) folder 
and the [experiments](experiments) folder. These folders contain various use cases and demonstrations 
of how to effectively use `PyDejaVu` for runtime verification.


## Output Files
After each execution of `PyDejaVu`, several output files are generated and stored in designated folders. 
These outputs are crucial for reviewing the results of the verification process and understanding the 
internal workings of the tool.

### Logs Folder:

The logs folder will contain the log file from the last execution. 
This log file is named with a timestamp to ensure that each run's output is distinct and easy to identify.

### Output Folder:

The output folder contains several important files generated during the verification process:
- `ast.dot`: A Graphviz source file used to create an abstract syntax tree (AST) graph for the specification. 
This file can be visualized using Graphviz to better understand the structure of the specification.
- `TraceMonitor.jar`: If the specification was compiled into a Java archive, this file will contain the 
compiled monitor.
- `TraceMonitor.scala`: If the specification was synthesized into Scala code, this file will be generated. 
It represents the synthesized monitor in Scala.
- `resultFile`: This file contains the results of the original DEJAVU execution, capturing the outcomes of 
the verification process. To ensure the `resultFile` is created correctly, 
notify DejaVu to close the result file by running `dejavu.verify.end_eval()`.
- `generated_trace.py`: This file is automatically generated when the user utilizes the CLI options. 
In this case, a `PyDejaVu` script is created in the working directory, 
tailored to the user's input parameters for runtime verification.

These output files provide a comprehensive overview of each execution, allowing you to analyze and debug the 
behavior of your specifications in detail.

## Contributors - For TP-DejaVu (Ordered by last name):
* [Klaus Havelund](http://www.havelund.com), Jet Propulsion Laboratory/NASA, USA
* [Moran Omer](https://github.com/moraneus), Bar Ilan University, Israel
* [Doron Peled](http://u.cs.biu.ac.il/~doronp), Bar Ilan University, Israel

