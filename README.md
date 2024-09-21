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

`PyDejaVu` bridges the gap between operational and declarative runtime verification, allowing users to define complex 
behaviors and verify them against formal specifications. Whether you're performing real-time analysis of event 
streams or ensuring that your system meets stringent correctness criteria, 
PyDejaVu offers a versatile solution that can be tailored to meet your needs.

With `PyDejaVu`, you can take advantage of Python's powerful capabilities in the first phase while relying 
on the declarative strength of DejaVu in the second phase, providing a comprehensive tool for runtime verification 
in a wide range of applications.

## Setting Up the Environment for PyDejavu
`PyDejaVu` is a Unix-compatible tool designed for cross-platform use, initially developed on macOS 
and tested on both macOS and Ubuntu Linux distributions. 
While specifically tested on these two platforms, `PyDejaVu` may potentially work on other Unix-like 
systems as well, though this would require further testing to confirm. 
It's important to note that as a Unix-based tool, `PyDejaVu` is not natively compatible with 
Windows and may require additional setup and modifications, to run on Windows machines. 

### Install Python

Ensure you have Python installed on your system. 
`PyDejavu` supports Python versions 3.8, 3.9, 3.10, 3.11, and 3.12.

### Install Java
`PyDejavu` requires Java, so install it on your system. 
You can use the OpenJDK distribution, specifically version 22 in this setup.
Install Java (Temurin distribution for Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y openjdk-22-jdk
```

After installation, set the `JAVA_HOME` environment variable to point to the Java installation directory:
```bash
export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```
Make sure to replace `/usr/lib/jvm/java-22-openjdk-amd64` with the path where Java is installed on your system.

### Install SDKMAN! and Scala

SDKMAN! is a tool for managing parallel versions of multiple SDKs, including Scala. 
Install SDKMAN! and then use it to install Scala version 2.12.18.
```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install scala 2.12.18
```
Set the `SCALA_HOME` environment variable to point to the Scala installation directory:

### Persist Environment Variables (Optional)

To make these environment variables persistent across sessions, add them to your shell's configuration file. 
For bash, this would be `~/.bashrc`, or for zsh, it would be `~/.zshrc`.
```bash
echo 'export JAVA_HOME=/usr/lib/jvm/java-22-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
echo 'export SCALA_HOME="$HOME/.sdkman/candidates/scala/current"' >> ~/.bashrc
echo 'export PATH=$SCALA_HOME/bin:$PATH' >> ~/.bashrc
```
After adding these lines, apply the changes with:
```bash
source ~/.bashrc  # or source ~/.zshrc if using zsh
```

### Verify Installation and Path Configuration

Verify that the installations and paths are set up correctly by checking the versions:
```bash
# Verify Python
python --version

# Verify Java
java -version

# Verify Scala
scalac -version
```
If these commands return the correct versions, your environment is correctly set up.

## PyDejaVu Installation

Before proceeding, ensure your environment is properly configured according to the instructions 
in the [previous section](#setting-up-the-environment-for-pydejavu). This step is crucial for the 
successful execution of `PyDejaVu` and helps prevent potential issues arising from an incorrectly 
set up environment.

Here we suggest three metods of installation:
- [**Pip Installation**](#pip-installation): 
For users who need to use `PyDejaVu` without making changes to the codebase, pip offers a quick 
and straightforward setup. 
This method allows you to focus on using the tool rather than managing its dependencies.
- [**Docker Installation**](#docker-installation): 
Docker provides a robust solution for running `PyDejaVu` in an isolated and consistent environment. 
This method is ideal for users who prefer not to modify their local system or manage package 
installations manually.
- [**Source Code Installation**](#source-code-installation): 
Installing the source code is a great option if you need more flexibility and control over the `PyDejaVu` project. 
Here are some reasons why you might choose this method:
  - **Customization and Modification:** If you plan to modify the code to suit specific requirements or contribute to the project, installing the source code gives you direct access to all the files. This is ideal for developers who want to extend or alter the functionality of `PyDejaVu`.
  - **Development and Debugging:** When working on new features or fixing bugs, having the source code installed locally allows you to test changes immediately. This setup is essential for contributors or developers actively working on the `PyDejaVu` project.
  - **Learning and Exploration:** If you're interested in understanding how `PyDejaVu` works internally, studying the source code can be very educational. You can explore the implementation details, experiment with changes, and see how different components interact.


### Pip Installation

#### Step 1: Install PyDejaVu

To install the latest version of `PyDejaVu` from PyPI, run:
```bash
pip install pydejavu-rv
```
This command will download and install `PyDejaVu` along with all its dependencies.

To upgrade an existing installation to the latest version:
```bash
pip install --upgrade pydejavu-rv
```

#### Step 2: Verify the Installation
After installation, verify that `PyDejaVu` has been installed correctly:
```bash
pip show pydejavu-rv
```
You should see output similar to:
```bash
Name: PyDejaVu-RV
Version: x.y.z
Summary: PyDejaVu is a Python implementation that wraps the original DejaVu jar file, providing a bridge between Python and the Java-based DejaVu runtime verification tool. This wrapper extends DejaVu's functionality by supporting a 2-phase monitoring approach.
Home-page: https://github.com/moraneus/pydejavu
Author: moraneus
Author-email: moraneus@gmail.com
License: Apache-2.0
Location: /path/to/your/python/site-packages
Requires: psutil, pyjnius, pytest, pytest-forked, pytest-xdist
```

#### 🛠️ Troubleshooting
If you encounter issues during installation or usage of `PyDejaVu`, consider the following:
 - **Python Environment**: Ensure your Python environment is correctly configured and you have 
   the necessary permissions to install packages.
 - **Virtual Environment**: If using a virtual environment, activate it before running 
   the pip install command:
    ```bash
    source path/to/your/venv/bin/activate
    ```
 - **Dependencies**: If you encounter dependency-related issues, try installing them separately
    ```bash
    pip install psutil pyjnius pytest pytest-forked pytest-xdist
    ```
 - **Version Conflicts**: In case of version conflicts, consider creating a new virtual environment 
   for a clean installation.
 - **System Requirements**: Ensure your system meets the requirements for running Java-based 
   applications, as `PyDejaVu` relies on a Java runtime.

### Docker Installation

#### Prerequisites
Ensure Docker is installed on your system. You can download 
Docker from [here](https://docs.docker.com/engine/install/).

#### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/moraneus/pydejavu.git
cd pydejavu
```

#### Step 2: Build the Docker Image

Ensure the Docker service is running, then build the image:

```bash
docker build -t pydejavu .
```
This command creates a Docker image named "pydejavu" with the following features:

- Ubuntu based environment for running `PyDejaVu`.
- Java and Scala installations.
- Python with Poetry for dependency management.
- `PyDejaVu` and its dependencies.
- Linter and tests run to ensure proper configuration.

You should see output similar to:
```bash
[+] Building 412.7s (17/17) FINISHED                                                                                                                                                                        
 => [internal] load build definition from Dockerfile                                                                                                                                                   0.0s
 => => transferring dockerfile: 2.32kB                                                                                                                                                                 0.0s
 => [internal] load .dockerignore                                                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                                                                                                    2.6s
 => [ 1/13] FROM docker.io/library/python:3.12-slim@sha256:XXXchecksumXXX                                                                           57.4s
 => => resolve docker.io/library/python:3.12-slim@sha256:XXXchecksumXXX                                                                              0.0s
 => => sha256:XXXchecksumXXX 9.12kB / 9.12kB                                                                                                         0.0s
 => => sha256:XXXchecksumXXX 1.75kB / 1.75kB                                                                                                         0.0s
 => => sha256:XXXchecksumXXX 5.11kB / 5.11kB                                                                                                         0.0s
 => => sha256:XXXchecksumXXX 29.16MB / 29.16MB                                                                                                       6.1s
 => => sha256:XXXchecksumXXX 3.33MB / 3.33MB                                                                                                         0.8s
 => => sha256:XXXchecksumXXX 13.38MB / 13.38MB                                                                                                      57.1s
 => => sha256:XXXchecksumXXX 250B / 250B                                                                                                             1.2s
 => => extracting sha256:XXXchecksumXXX                                                                                                              0.5s
 => => extracting sha256:XXXchecksumXXX                                                                                                              0.1s
 => => extracting sha256:XXXchecksumXXX                                                                                                              0.3s
 => => extracting sha256:XXXchecksumXXX                                                                                                              0.0s
 => [ 2/13] RUN apt-get update && apt-get install -y     curl     wget     gnupg2     software-properties-common     unzip     zip     && rm -rf /var/lib/apt/lists/*                                 21.8s
 => [ 3/13] RUN wget -O- https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /usr/share/keyrings/adoptium.asc     && echo "deb [signed-by=/usr/share/keyrings/adoptium.asc] https://  179.2s
 => [ 4/13] RUN curl -s "https://get.sdkman.io" | bash     && bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install scala 2.12.18"                                                          14.6s 
 => [ 5/13] RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && scalac -version && java -version && python --version"                                                                              0.6s 
 => [ 6/13] RUN pip install --no-cache-dir "poetry==1.6.1"                                                                                                                                            18.4s 
 => [ 7/13] RUN poetry config virtualenvs.create false                                                                                                                                                 0.5s 
 => [ 8/13] RUN pip install flake8                                                                                                                                                                     2.5s 
 => [ 9/13] RUN git clone https://github.com/moraneus/pydejavu.git /app                                                                                                                               20.1s 
 => [10/13] WORKDIR /app                                                                                                                                                                               0.0s 
 => [11/13] RUN poetry install --no-interaction --no-ansi                                                                                                                                              2.2s 
 => [12/13] RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && flake8 . --count --exit-zero --max-complexity=10 --max-line  0.7s 
 => [13/13] RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && pytest --forked"                                                                                                                  90.6s 
 => exporting to image                                                                                                                                                                                 1.4s 
 => => exporting layers                                                                                                                                                                                1.4s 
 => => writing image sha256:XXXchecksumXXX                                                                                                           0.0s 
 => => naming to docker.io/library/pydejavu     
```

#### Step 3: Run the Docker Container
Start an interactive session in the Docker container:
```bash
docker run -it pydejavu
```
This command starts an interactive session inside the Docker container, 
where `PyDejaVu` is set up and ready to use.

#### Step 4: Operate PyDejaVu
Inside the Docker container, you can run `PyDejaVu` commands. For example:

##### Example: Using the CLI
```bash
cd examples/cli
python -m pydejavu --bits 20 --stats true --qtl sample.qtl --operational sample.pqtl --trace sample.log
```

##### Example: Running a Pre-defined Monitor
```bash
cd examples/pydejavu_monitors
python monitor_for_detecting_suspicious_login_patterns.py
```

#### 🛠️ Troubleshooting

- **Docker Service**: Ensure the Docker service is running before building or running containers.
- **Persistent Storage**: To persist data between container runs, use Docker volumes:
    ```bash
    docker run -it -v /path/on/host:/path/in/container pydejavu
    ```
- **Resource Allocation**: If `PyDejaVu` requires more resources, allocate them using Docker's resource flags:
    ```bash
    docker run -it --cpus 2 --memory 4g pydejavu
    ```
- **Cached Images**: If the Docker build command completes unusually quickly (within a few seconds), 
    it's likely using cached images from previous builds. In this case, you may need to 
    remove the older Docker containers and images associated with your project 
    (in this case, `pydejavu`) to force a fresh build. Here's how you can do this:
  1. Stop and remove existing containers:
     ```bash
     docker stop $(docker ps -a -q --filter ancestor=pydejavu)
     docker rm $(docker ps -a -q --filter ancestor=pydejavu)
     ```
  2. Remove associated images:
       ```bash
     docker rmi $(docker images | grep pydejavu | awk '{print $3}')
     ```
  3. Rebuild your Docker image:
     ```bash
     docker build --no-cache -t pydejavu .
     ```
  This process ensures that your next build will create a fresh image 
  without relying on potentially outdated cached layers.

- **Debugging**: To debug issues, you can start a shell in the container:
    ```bash
    docker run -it pydejavu /bin/bash
    ```

### Source Code Installation

#### Prerequisites

Ensure that you have Python 3.8 or higher installed on your system. 

#### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/moraneus/pydejavu.git
cd pydejavu
```

#### Step 2: Install Poetry
This project uses [Poetry](https://python-poetry.org/) for managing dependencies and packaging. 
Follow these steps to set up your development environment:

1. Create and activate a virtual environment (recommended):
    ```bash
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    ```
2. Install Poetry:
    ```bash
    pip install poetry
    ```
3. Verify the installation:
    ```bash
    poetry --version
    ```
    If Poetry is correctly installed, you should see the version number.

#### Step 3: Install Project Dependencies
With Poetry installed, you can now install the project dependencies.
Run the following command in the root directory of the project:
```bash
poetry install
```
This will create a `poetry.lock` file and install all necessary dependencies for the project.

#### 🛠️ Troubleshooting
If you encounter issues during installation or while running the project, consider the following:

 - Ensure that your Python version meets the minimum requirement.
 - Check that Poetry is correctly installed and accessible from your command line. 
 - Verify that all dependencies are properly installed by running poetry show.

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
python3 -m pydejavu --bits 20 --stats true --qtl /path/to/spec.qtl --operational /path/to/events.pqtl --trace /path/to/trace.log
```

This command initializes the monitor with 20 bits, enables statistics, 
and uses the specified qtl, operational, and trace files for runtime verification.


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


## Examples
You can find comprehensive examples of monitors in the [examples](https://github.com/moraneus/pydejavu/tree/main/examples/pydejavu_monitor) folder 
and the [experiments](https://github.com/moraneus/pydejavu/tree/main/experiments) folder. These folders contain various use cases and demonstrations 
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
notify DejaVu to close the result file by running `dejavu.end()`.
- `generated_trace.py`: This file is automatically generated when the user utilizes the CLI options. 
In this case, a `PyDejaVu` script is created in the working directory, 
tailored to the user's input parameters for runtime verification.

These output files provide a comprehensive overview of each execution, allowing you to analyze and debug the 
behavior of your specifications in detail.

## Contributors - For `PyDejaVu` (Ordered by last name):
* [Klaus Havelund](http://www.havelund.com), Jet Propulsion Laboratory/NASA, USA
* [Moran Omer](https://github.com/moraneus), Bar Ilan University, Israel
* [Doron Peled](http://u.cs.biu.ac.il/~doronp), Bar Ilan University, Israel

