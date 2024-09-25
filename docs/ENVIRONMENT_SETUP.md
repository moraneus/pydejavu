# Environment Setup for PyDejavu

`PyDejaVu` is a Unix-compatible tool designed for cross-platform use, initially developed on macOS 
and tested on both macOS and Ubuntu Linux distributions. 
While specifically tested on these two platforms, `PyDejaVu` may potentially work on other Unix-like 
systems as well, though this would require further testing to confirm. 
It's important to note that as a Unix-based tool, `PyDejaVu` is not natively compatible with 
Windows and may require additional setup and modifications, to run on Windows machines. 

## Install Python

Ensure you have Python installed on your system. 
`PyDejavu` supports Python versions 3.8, 3.9, 3.10, 3.11, and 3.12.
For more information of how to install Python visit the [Python official website](https://www.python.org/).

## Install Java
`PyDejavu` requires Java to run, 
so you need to install it on your system. We recommend using the OpenJDK distribution.
During development, we used Java version 22, but older versions should work as well.
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

## Install SDKMAN! and Scala

SDKMAN! is a tool for managing parallel versions of multiple SDKs, including Scala. 
Install SDKMAN! and then use it to install Scala version 2.12.18.

👉 **Note**: Since `DejaVu` supports only Scala version 2.X.X due to its limitations, 
we have used Scala 2.X.X in our setup.
```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install scala 2.12.18
```

Set the `SCALA_HOME` environment variable to point to the Scala installation directory:
```bash
export SCALA_HOME="$HOME/.sdkman/candidates/scala/current
export PATH=$SCALA_HOME/bin:$PATH
```

## Persist Environment Variables (Optional)

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

## Verify Installation and Path Configuration

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