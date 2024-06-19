# Description

An over-engineered gantt chart for phd projects (or other long and individual projects). Includes options for adding interruptions and different views of the gantt chart so that you can download to a pdf and send to your supervisors. Alternatively you can share the web-app version and instruction for setting that up are included.

## Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* Python (version 3.10 or higher recommended).
* [Poetry](https://python-poetry.org/docs/) for dependency management and packaging.
* (Optional) `pyenv` for managing multiple Python versions.

### Step 1: Clone the Repository

First, clone the project repository to your local machine using Git. Open a terminal and run:

```sh
git clone https://github.com/carrowmw/phd-gantt-chart
cd phd-project
```

### Step 2: (Optional) Setting Up Python with `pyenv`

If you prefer to manage multiple Python versions on your system, you can use `pyenv` to install and set a specific Python version for this project:

```sh
pyenv install 3.10.0  # Skip if already installed
pyenv local 3.10.0
```

### Step 3: Installing Dependencies with Poetry

With Poetry installed, set up the project's dependencies by running the following command in the project root directory

```sh
poetry install
```

### Step 4: Activating the Virtual Environment

After installing the dependencies, you can activate the project's virtual environment using Poetry:

```sh
poetry shell
```

### Step 5: (Optional) Installing Development Dependencies with Poetry

For developers and contributors looking to run tests or use development tools, ensure you've installed the project's development dependencies:

```sh
poetry install --with dev
```

This includes additional packages like `pytest` for testing and code2flow for generating flowcharts from your code.

To run tests, you can use the following command:

```sh
pytest
```

## Running the Project

After installing the dependencies and activating the virtual environment, you can now run the project as follows: