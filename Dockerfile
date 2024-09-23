# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables for Python and Poetry
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.6.1

# Install basic dependencies and tools including zip and unzip
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg2 \
    software-properties-common \
    unzip \
    zip \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Add gtime alias
RUN echo "alias gtime='time'" >> ~/.bashrc

# Add the Adoptium repository and install Java (Temurin JDK)
RUN wget -O- https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /usr/share/keyrings/adoptium.asc \
    && echo "deb [signed-by=/usr/share/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb/ jammy main" | tee /etc/apt/sources.list.d/adoptium.list \
    && apt-get update && apt-get install -y temurin-22-jdk git

# Install SDKMAN! and Scala
RUN curl -s "https://get.sdkman.io" | bash \
    && bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && sdk install scala 2.12.18"

# Set environment variables for Scala
ENV SCALA_HOME="$HOME/.sdkman/candidates/scala/current"
ENV PATH="$PATH:$SCALA_HOME/bin"

# Make sure Scala is sourced properly
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && scalac -version && java -version && python --version"

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Install flake8 (or any additional Python dependencies you need globally)
RUN pip install flake8

# Clone the repository
RUN git clone https://github.com/moraneus/pydejavu.git /app

# Set working directory
WORKDIR /app

# Install Python dependencies from the cloned repository using Poetry
RUN poetry install --no-interaction --no-ansi

# Ensure SDKMAN environment is sourced before running linter and tests
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics"

# Run tests using pytest (ensure Scala environment is sourced)
RUN bash -c "source $HOME/.sdkman/bin/sdkman-init.sh && pytest --forked"

# Set the default command (if you want the container to execute something by default)
CMD ["bash"]
