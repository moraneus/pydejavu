# PyDejaVu

![pydejavu.png](extra%2Fimages%2Fpydejavu.jpg)
PyDejaVu is a Python library that wraps the original [DejaVu](https://github.com/havelund/dejavu/tree/master) binary, 
providing a bridge between Python and the 
Java-based DejaVu runtime verification tool. It is a powerful tool designed for two-phase 
Runtime Verification (RV) processing, similar to the [Tp-DejaVu](https://github.com/moraneus/TP-DejaVu) tool, 
combining the flexibility and expressiveness of 
Python with the rigorous, declarative monitoring capabilities of 
the DejaVu tool.

#### Two-Phase Runtime Verification

PyDejaVu operates in two distinct phases:

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

Ensure that you have Python 3.7 or higher installed on your system. 
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
pip install pydejavu
```
This command will automatically download and install `PyDejaVu` and all its dependencies.

If you need to upgrade `PyDejaVu` to the latest version, you can do so with:
```bash
pip install --upgrade pydejavu
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

## Usage

`PyDejaVu` is a versatile tool that bridges Python's operational capabilities with the rigorous, 
declarative runtime verification offered by the DEJAVU tool. Below is an example demonstrating how to 
use `PyDejaVu` for two-phase Runtime Verification (RV) processing, allowing you to monitor properties of 
event streams using both Python and DEJAVU's first-order logic specifications.

### Example Usage

### Step 1: Import the Library

To get started with `PyDejaVu`, you first need to import the relevant classes from the library. 
Typically, you will need the `Monitor` class, which is the core component of the `PyDejaVu` library.

```python
from pydejavu.core.monitor import Monitor
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
Create an instance of the Monitor class, passing in your specification and other optional parameters. 
The Monitor constructor allows you to customize several aspects of the runtime verification process:

- `i_spec`: The specification string that defines the properties you want to monitor.
- `i_bits`: The number of bits used in verification. This can influence the performance and accuracy of the 
verification process. The default is 20 bits.

- `i_mode`: An optional parameter that specifies the mode of operation. This could be used to toggle between 
different verification output modes.
  - `debug`: This option is used to enable comprehensive logging and diagnostic messages that help developers 
  understand the internal workings of the monitoring process, track down issues, and verify the correctness of the 
  implementation. This debug output is crucial during development and troubleshooting to ensure the logic behaves as 
  expected.
  - `profile`: This option is used to enable detailed performance profiling of the monitored properties, 
  recording metrics that can be analyzed to understand the efficiency and complexity of the property evaluations.

- `i_statistics`: A boolean flag that, if set to True, enables the collection of statistics during the verification 
process. The default is False.

- `i_logger`: An optional logger instance for customized logging. If not provided, a default logger will be used.

Here’s how you can initialize the Monitor:

```python
dejavu = Monitor(i_spec=specification, i_bits=8)
dejavu.init_monitor()
```

#### Alternative Options for Monitor Initialization
While initializing a Monitor in `PyDejaVu` using a specification is common, you also have the flexibility to 
initialize the monitor using a pre-synthesized Scala monitor or a compiled monitor JAR file. 
These options are particularly useful when you already have a monitor synthesized or compiled outside of the 
typical specification-based workflow.

##### Option 1: Initializing with a Synthesized Scala Monitor
In this option, you initialize the Monitor and then compile a Scala monitor file that has already been synthesized.
```python
# Initialize the Monitor with custom settings
dejavu = Monitor(i_bits=20, i_statistics=False)

# Compile the synthesized Scala monitor
compile_jar_path = dejavu.compile_monitor('/path/to/TraceMonitor.scala')

# Update monitor spec names - this is mandatory when the specification is not synthesized from scratch
dejavu.spec_names = ['example']

# Link the monitor to the compiled JAR file
dejavu.linkage_monitor(compile_jar_path)
```

##### Option 2: Initializing with a Pre-Compiled Monitor JAR
If you already have a compiled monitor in the form of a JAR file, you can directly link this JAR file to the 
Monitor after initialization.
```python
# Initialize the Monitor with custom settings
dejavu = Monitor(i_bits=20, i_statistics=False)

# Update monitor spec names - this is mandatory when the specification is not synthesized from scratch
dejavu.spec_names = ['example']

# Link the monitor directly to the pre-compiled JAR file
dejavu.linkage_monitor('/path/to/TraceMonitor.jar')
```

### Step 4: Sharing Data Between Handlers
When handling events, you may need to share data between different event handlers. 
There are two primary ways to achieve this in PyDejaVu:

##### Global Variables:
 - You can use global variables to store and share data between handlers. 
This approach is straightforward and effective when the data to be shared is simple and doesn't need to 
persist beyond the lifetime of the program.
##### `PyDejaVu` Shared Variables API:
- `PyDejaVu` provides a built-in API for managing shared variables, which is particularly useful for more 
complex scenarios or when you want to maintain state across different parts of your program. 
- You can store and retrieve shared data using `dejavu.set_shared("key", value)` and `dejavu.get_shared("key", default_value)` 
respectively. This method ensures that your data is managed within the `PyDejaVu` framework, offering more 
control and avoiding potential issues with global variables.
- For example:
    ```python
    dejavu.set_shared("last_seen_q", False)
    last_seen_q = dejavu.get_shared("last_seen_q", False)
    ```
- Another type of shared variable function is the `dejavu.last_eval("spec_name")` function which is a powerful feature 
that allows you to access the last evaluation result of a specified property. This can be especially useful 
within your event handlers when you need to consider the declarative verdict in your operational logic.
For example, within an handler function, you can check the last evaluation result of property "example" before 
making further decisions:
    ```python
  verdict = dejavu.last_eval("example")
  if verdict:
  # Perform additional operations based on the last evaluation result
    pass

    ```


### Step 5: Define Operational Event Handlers
Define Python functions to handle the events specified in your logic. 
These handlers perform real-time operations on the events, such as arithmetic calculations, string manipulations, 
or state tracking. The handlers are decorated with the `@dejavu.operational("event_name")` decorator, 
linking them to specific events in your specification.

```python
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
```
This code defines two operational event handlers, `handle_p` and `handle_q`, which are responsible for processing 
events named **"p"** and **"q"** respectively. 
These handlers are part of the two-phase runtime verification process facilitated by `PyDejaVu`, 
where events are processed in real-time using Pythonic operations, and the results can influence 
the monitoring and verification against a formal specification.

The `@dejavu.operational("p")` decorator is used to link the `handle_p` function to the event **"p"**. 
When an event named **"p"** is encountered in the event stream, `PyDejaVu` will automatically call the `handle_p` 
function to process it.  The `handle_p(arg_x: int)` function is designed to handle the **"p"** event. 
It takes an integer argument `arg_x` and uses the global variables `y` and `last_seen_q` to perform its operations.

Similarly, the `@dejavu.operational("q")` decorator links the `handle_q` function to the **"q"** event, 
ensuring that this function is called when a **"q"** event is encountered.

### Step 6: Process Event Streams
You can now process streams of events using `PyDejaVu`. 
For instance, you can read events from a log file in chunks and pass them to the monitor for processing. 
The monitor will evaluate the events against your specifications.
```python
for chunk in dejavu.read_bulk_events('/path/to/trace/file', chunk_size=1000):
    results = dejavu.verify.process_events(chunk)
    dejavu.logger.debug(f"Processed chunk of {len(chunk)} events")
    for result in results:
        dejavu.logger.debug(result)
```
You are not required to use the event iteration API to process events in `PyDejaVu`. 
Instead, you have the flexibility to process events individually or in batches using the following methods:

- Processing Multiple Events:
You can use the `dejavu.verify.process_events(events)` method to process a batch of events at once. 
This method is particularly useful when you have a list of events that need to be verified together.

- Processing a Single Event:
Alternatively, you can use the `dejavu.verify.process_event(event)` method to process a single event whenever needed. 
This allows you to handle events as they occur in real-time or in specific scenarios where events are 
processed one at a time.

🔔 Each event must be a dictionary of type `Dict[str, Any]`. The dictionary should include at least two keys:
- `name`: The name of the event.
- `args`: A list or dictionary containing the arguments associated with the event.

An event for example can look as follows: `{'name': 'key', 'args': [arg1, arg2, ...]}`.

When processing multiple events, you should provide a list of such dictionaries 
(i.e., `List[Dict[str, Any]]`). 
This structure ensures that each event is correctly recognized and processed by the `PyDejaVu` verification engine.

A whole monitor examples can be found in the [examples](examples%2Fpydejavu_monitor) folder.

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
the verification process.

These output files provide a comprehensive overview of each execution, allowing you to analyze and debug the 
behavior of your specifications in detail.

## Contributors - For TP-DejaVu (Ordered by last name):
* [Klaus Havelund](http://www.havelund.com), Jet Propulsion Laboratory/NASA, USA
* [Moran Omer](https://github.com/moraneus), Bar Ilan University, Israel
* [Doron Peled](http://u.cs.biu.ac.il/~doronp), Bar Ilan University, Israel

