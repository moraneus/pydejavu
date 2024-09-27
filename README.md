# PyDejaVu

![PyPI](https://img.shields.io/pypi/v/PyDejaVu-RV)
![PyPI - Downloads](https://img.shields.io/pypi/dm/PyDejaVu-RV)
[![License: MIT](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](https://opensource.org/license/apache-2-0)

![pydejavu.png](https://raw.githubusercontent.com/moraneus/pydejavu/main/extra/images/pydejavu.jpg)

`PyDejaVu` is a Python library that wraps the original [DejaVu](https://github.com/havelund/dejavu/tree/master) binary, 
providing a bridge between Python and the 
Scala-based (and JVM-based) DejaVu runtime verification tool. It is a powerful tool designed for two-phase 
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
   past time temporal logic specification. This phase ensures that the runtime behavior conforms to the formal properties 
   defined in the specification. By integrating with DejaVu, `PyDejaVu` provides a robust framework for verifying 
   that the system adheres to specified safety properties, making it suitable for applications requiring 
   high levels of assurance.


## PyDejaVu Installation

`PyDejaVu` is a Unix-compatible tool designed for cross-platform use, initially developed on macOS 
and tested on both macOS and Ubuntu Linux distributions. 
While specifically tested on these two platforms, `PyDejaVu` may potentially work on other Unix-like 
systems as well, though this would require further testing to confirm. 
It's important to note that as a Unix-based tool, `PyDejaVu` is not natively compatible with 
Windows and may require additional setup and modifications, to run on Windows machines.

Here we suggest three methods of installation:
- [**Pip Installation**](#pip-installation): 
For users who need to use `PyDejaVu` without making changes to the codebase, pip offers a quick 
and straightforward setup. 
This method allows you to focus on using the tool rather than managing its dependencies.
- [**Docker Installation**](#docker-installation): 
Docker provides a robust solution for running `PyDejaVu` in an isolated and consistent environment. 
This method is ideal for users who prefer not to modify their local system or manage package 
installations manually.
With Docker, you don't need to prepare your system for running `PyDejaVu`, as the Docker image comes 
pre-packaged with all the necessary Scala and Java dependencies required for `DejaVu`.
- [**Source Code Installation**](#source-code-installation): 
Installing the source code is a great option if you need more flexibility and control over the `PyDejaVu` project. 
Here are some reasons why you might choose this method:
  - **Customization and Modification:** If you plan to modify the code to suit specific requirements or contribute to the project, installing the source code gives you direct access to all the files. This is ideal for developers who want to extend or alter the functionality of `PyDejaVu`.
  - **Development and Debugging:** When working on new features or fixing bugs, having the source code installed locally allows you to test changes immediately. This setup is essential for contributors or developers actively working on the `PyDejaVu` project.
  - **Learning and Exploration:** If you're interested in understanding how `PyDejaVu` works internally, studying the source code can be very educational. You can explore the implementation details, experiment with changes, and see how different components interact.


### Pip Installation

👉 Before proceeding, ensure your environment is properly configured according to the instructions 
in the [environment setup guide](docs/ENVIRONMENT_SETUP.md). This step is crucial for the 
successful execution of `PyDejaVu` and helps prevent potential issues arising from an incorrectly 
set up environment.

#### Step 1: Create Virtual Environment
Creating a virtual environment is highly recommended when installing `PyDejaVu`. 
A virtual environment isolates your project's dependencies from the global Python installation, 
preventing package conflicts and making dependency management easier.

Create the Virtual Environment:
```bash
python3 -m venv pydejavu-env
```
This command creates a new directory called pydejavu-env containing the isolated Python environment.

Activate the Virtual Environment:
```bash
source pydejavu-env/bin/activate
```
After activation, your command prompt will change to indicate that you are now using the virtual environment.

👉**Note**: Remember to activate the virtual environment each time you start a new session to 
ensure you are using the isolated environment.

#### Step 2: Install PyDejaVu

With the virtual environment activated, install the latest version of `PyDejaVu` from PyPI:
```bash
pip install pydejavu-rv
```
This command will download and install `PyDejaVu` along with all its dependencies into your virtual environment.

To upgrade an existing installation to the latest version:
```bash
pip install --upgrade pydejavu-rv
```

#### Step 3: Verify the Installation
After installation, verify that `PyDejaVu` has been installed correctly:
```bash
pip show pydejavu-rv
```
This command should display details about the `PyDejaVu` package, confirming a 
successful installation within your virtual environment.
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

#### Step 4: Operate PyDejaVu
To test the library and explore the capabilities of `PyDejaVu`, 
you can download the 
[experiments archive](https://raw.githubusercontent.com/moraneus/pydejavu/main/experiments/experiments.zip), 
which contains the experiments 
used in our paper. This archive includes three folders named `example_1`, `example_2` and  `example_3`, 
each corresponding to a different experiment. Each example folder contains all the necessary 
files to run the experiment.

- Extract the [experiments.zip](https://raw.githubusercontent.com/moraneus/pydejavu/main/experiments/experiments.zip) 
  file:
    ```bash
    unzip experiments.zip
    ```
- Change directory to the example folder you wish to run:
    ```bash
    cd example_X
    ```
   Replace `X` with the example number (1 to 3).

- Execute the experiment using the provided bash script. **Make sure you are execute it from the virtual environment**.
    ```bash
    ./run_experiment
    ```
  In some cases, if `run_experiment` cannot be run, you need to make it executable using the following command:
    ```bash 
    chmod +x run_experiment
    ```
  This script automates the execution of all experiments within the specified `example_X` folder. 
  It sequentially runs the experiments using different log files to evaluate PyDejaVu's performance 
  across varying trace sizes (10K, 100K, 500K, and 1M). Upon completion, the results will be saved 
  in a file named `result-spec-X`.

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
The Docker installation process automatically clones the latest `PyDejaVu` source code inside 
the container. Unlike the standard installation method, it does not use the `pip install 
pydejavu-rv` command. Instead, it builds and installs `PyDejaVu` directly from the cloned 
source code within the Docker environment. 
This approach ensures that you are running the most recent version of `PyDejaVu`,
including the latest features and updates that may not yet be available through PyPI.


#### Prerequisites
Ensure Docker is installed. You can download 
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
This command creates a Docker image named "pydejavu" (based on a `Dockerfile` located in the root project folder)
with the following features:

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
Inside the Docker container, you can use `PyDejaVu` with no addition configuration. For example:

##### Example: Running a Pre-defined Monitor
```bash
cd /app/examples/pydejavu_monitor
python monitor_for_detecting_suspicious_login_patterns.py
```

##### Example: Using the CLI
```bash
cd /app/examples/cli
python -m pydejavu --bits 20 --stats true --qtl sample.qtl --operational sample.pqtl --trace sample.log
```

##### Example: Experiments
Since we are using the `PyDejaVu` source code inside the Docker container 
we have direct access to the experiment folders.

- Change directory to the experiment folder you wish to test:
    ```bash
    cd /app/experiments/example_X
    ```
   Replace `X` with the example number (1 to 3).

- Execute the experiments using the provided bash script:
    ```bash
    bash -i run_experiment
    ```
This script automates the execution of all experiments within the specified `example_X` folder. 
It sequentially runs the experiments using different log files to evaluate PyDejaVu's performance 
across varying trace sizes (10K, 100K, 500K, and 1M). Upon completion, the results will be saved 
in a file named `result-spec-X`.

#### 🛠️ Troubleshooting

- **Docker Service**: Ensure the Docker service is running before building or running containers.
- **Persistent Storage**: To persist data between container runs and share files between your host
    machine and the Docker container, you can use Docker volumes. 
    This is particularly useful when you have predefined `PyDejaVu` monitor files or other 
    resources on your local machine that you want to use inside the container without 
    copying or rewriting them:
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

👉 Before proceeding, ensure your environment is properly configured according to the instructions 
in the [environment setup guide](docs/ENVIRONMENT_SETUP.md). This step is crucial for the 
successful execution of `PyDejaVu` and helps prevent potential issues arising from an incorrectly 
set up environment.

#### Step 1: Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/moraneus/pydejavu.git
cd pydejavu
```

#### Step 2: Install Poetry
This project uses [Poetry](https://python-poetry.org/) for managing dependencies and packaging. 
Follow these steps to set up your development environment:

1. Create and activate a virtual environment:
    ```bash
    python3 -m venv pydejavu-env
    source pydejavu-env/bin/activate
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

#### Step 4: Operate PyDejaVu
After the installation is finished we can use `PyDejaVu` with no addition configuration.

##### Example: Running a Pre-defined Monitor
👉**Note**: Make sure you are in the root directory of `PyDejaVu`.
```bash
cd examples/pydejavu_monitor
python monitor_for_detecting_suspicious_login_patterns.py
```

##### Example: Using the CLI
👉**Note**: Make sure you are in the root directory of `PyDejaVu`.
```bash
cd /app/examples/cli
python -m pydejavu --bits 20 --stats true --qtl sample.qtl --operational sample.pqtl --trace sample.log
```

##### Example: Experiments
Since we are using the `PyDejaVu` source code we have direct access to the experiment folders.

👉**Note**: Make sure you are in the root directory of `PyDejaVu`.
- Change directory to the experiment folder you wish to test:
    ```bash
    cd experiments/example_X
    ```
   Replace `X` with the example number (1 to 3).

- Execute the experiments using the provided bash script:
    ```bash
    ./run_experiment
    ```
This script automates the execution of all experiments within the specified `example_X` folder. 
It sequentially runs the experiments using different log files to evaluate PyDejaVu's performance 
across varying trace sizes (10K, 100K, 500K, and 1M). Upon completion, the results will be saved 
in a file named `result-spec-X`.


#### 🛠️ Troubleshooting
If you encounter issues during installation or while running the project, consider the following:

 - Ensure that your Python version meets the minimum requirement.
 - Check that Poetry is correctly installed and accessible from your command line. 
 - Verify that all dependencies are properly installed by running poetry show.

## Usage

In this section, we present a simple usage of the tool divided into two 
examples. The first example demonstrates how users can easily operate `DejaVu` directly 
from `PyDejaVu`. The second example builds upon the first, showing how to enhance the 
expressiveness of your application by leveraging the power of `PyDejaVu`. 
By leverages `DejaVu`'s capabilities, `PyDejaVu` involves a few steps before it starts 
the evaluation process. First, it analyzes and parses the specification to ensure it 
meets the syntax of QTL (Quantified Temporal Logic). 
Then, it compiles a Scala-based monitor. 
This Scala compilation step may take some time, so don't be alarmed if there is a delay 
during this process.
For more advanced usage and explanations, please refer to the [documentation](docs/ADVANCED_USAGE.md).


### Example 1
Consider a simple filesystem mechanism that handles several key events. The filesystem
allows opening a file with the an `open(F, f, m, s)`, carrying as arguments the
folder name `F`, the filename `f` (technically a file id), the access mode `m` (read or write), and the size
`s` which is the maximal number of bytes that can be written. The `close(f)` event
indicates that a file `f` has been closed. The write event `write(f, d)` contains the
filename and the data `d` (a string) being written. Additionally, the system
supports `create(F)` and `delete(F)` events, which represent the creation or deletion
of a folder.
The requirement we are verifying states that if data is written to a file, the
file must have been opened in write mode, not closed since, and must reside in
a folder that has been created and not deleted since.

```python
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
    {"name": "open", "args": ["tmp", "f1", "w", "5"]},
    {"name": "write", "args": ["f1", "some text"]},
    {"name": "close", "args": ["f1"]},
    {"name": "delete", "args": ["tmp"]}
]

for e in events:
    monitor.verify(e)
monitor.end()
```

This code snippet demonstrates how to operate `DejaVu` directly 
from `PyDejaVu` to perform runtime verification based on a formal specification written in first-order 
past time temporal logic.
First, the Monitor class is imported from `pydejavu.core.monitor`,
and the specification, named as `example`, is defined as a multi-line string. 
The monitor is then initialized with this specification, setting up the verification environment.
A list of events is created to simulate a sequence of I/O operations: creating a folder (`create`), 
opening a file (`open`), writing to it (`write`), closing it (`close`), 
and finally deleting the hosting folder (`delete`). 
Each event is a dictionary containing the event name and its arguments.
The events are processed in a loop where each event is passed to the `monitor.verify(e)` method. 
In this case, where no event handlers are defined, the events are forwarded directly to the declarative phase 
for verification against the specification. 
After all events are processed, `monitor.end()` is called to finalize the evaluation.
This step is crucial for obtaining statistics results and for the monitor 
to release resources appropriately.

#### Example 1 Output
As shown in the following output snippet, this example reports no errors.

```bash
0 errors detected!

==================
  Event Counts:
------------------
  create : 1
  open   : 1
  delete : 1
  close  : 1
  write  : 1
==================

- Garbage collector was not activated
```


### Example 2

```python
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
    {"name": "open", "args": ["tmp", "f1", "w", "5"]},
    {"name": "write", "args": ["f1", "some text"]},
    {"name": "close", "args": ["f1"]},
    {"name": "delete", "args": ["tmp"]}
]

for e in events:
    monitor.verify(e)
monitor.end()
```

This code differs from the previous example by incorporating operational event handlers that 
perform real-time computations and state management before events are passed to the 
declarative phase for verification. In the earlier code, events were directly forwarded to 
the declarative phase without any operational processing. 
Here, the `@event` decorator is used to define custom handlers for the `open`, `close`,
and `write` events, enabling the code to maintain and manipulate state during the operational 
phase. Generally, the handlers are decorated with the `@event("event_name")` decorator, 
linking them to specific events in your specification.
This definition is optional; if no handler is defined for a specific event, `PyDejaVu` will forward the 
event directly to DejaVu for evaluation. Without any handler definitions, PyDejaVu functions 
the same as `DejaVu` without the operational phase.

A key difference is the introduction of the `total_sizes` dictionary, 
which tracks the remaining allowed write sizes for each file. 
In the `open` handler, the code checks if the file is opened in write mode `"w"` and 
initializes the total allowed size `s` for that file in the `total_sizes` dictionary. 
The `write` handler then uses this information to ensure that the length of the data 
being written does not exceed the remaining allowed size. 
It calculates the length of the data `d`, compares it against the remaining size for the file, 
and updates the `total_sizes` accordingly. 
If the `write` operation exceeds the allowed size, an `ok` flag is set to `False`, 
indicating that the `write` is not permitted.

These operational event handlers allow for immediate enforcement of constraints and 
preliminary checks before events are evaluated against the formal specification in 
the declarative phase. By performing these computations upfront, the code can prevent 
invalid or undesirable events from proceeding further, enhancing efficiency and providing 
immediate feedback. This integration of operational logic with declarative specifications 
showcases how `PyDejaVu` increases the expressiveness of the system, enabling more complex 
and nuanced runtime verification scenarios compared to the previous example where such 
operational checks were absent.

#### Example 2 Output
As shown in the following output snippet, this example reports one error because it failed when
attempting to write the `"some text"` string into `f1`, which is limited to 5 characters.

```bash
1 errors detected!

==================
  Event Counts:
------------------
  create : 1
  open   : 1
  delete : 1
  close  : 1
  write  : 1
==================

- Garbage collector was not activated
```

### More Usage Examples
You can find more comprehensive usage examples of monitors in the [examples](https://github.com/moraneus/pydejavu/tree/main/examples/pydejavu_monitor) folder 
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

The `output` folder contains several important files generated during the verification process:
- `ast.dot`: A Graphviz source file used to create an abstract syntax tree (AST) graph for the specification. 
This file can be visualized using Graphviz to better understand the structure of the specification.
- `TraceMonitor.jar`: If the specification was compiled into a Java archive, this file will contain the 
compiled monitor.
- `TraceMonitor.scala`: If the specification was synthesized into Scala code, this file will be generated. 
It represents the synthesized monitor in Scala.
- `resultFile`: This file is primarily used in unit testing to compare the expected errors with 
the actual errors encountered. It contains the results of the original `DejaVu` execution, 
capturing any errors from the verification process. When an error occurs, the event index is 
written to this file. However, be aware that the `resultFile` remains empty if no errors 
are detected during verification. To ensure the `resultFile` is created correctly, 
make sure to run `monitor.end()` to notify `DejaVu` to close the result file and finalize 
the execution.
- `generated_trace.py` (Optional): This file is automatically generated when the user utilizes the CLI options. 
In this case, a `PyDejaVu` script is created in the working directory, 
tailored to the user's input parameters for runtime verification.

These output files provide a comprehensive overview of each execution, allowing you to analyze and debug the 
behavior of your specifications in detail.

```bash
output/
├── ast.dot
├── TraceMonitor.jar
├── TraceMonitor.scala
├── resultFile
└── generated_trace.py  (Optional)
```

## Contributors - For `PyDejaVu` (Ordered by last name):
* [Klaus Havelund](http://www.havelund.com), Jet Propulsion Laboratory/NASA, USA
* [Moran Omer](https://github.com/moraneus), Bar Ilan University, Israel
* [Doron Peled](http://u.cs.biu.ac.il/~doronp), Bar Ilan University, Israel

