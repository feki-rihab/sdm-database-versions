# Python package: sdm-database-versions  
This package create a database of Smart Data Models versions in order to achieve functionalities like tracking the history of change in SDMs &amp; tracing the evolution of SDMs in every version upgrade.

# Poetry Initialization - Running the Project Locally 

To manage the dependencies in this project and for Python package management, Poetry is used. 

1. **Install Poetry:** 
Execute the following command in the terminal: 

    ```shell
    curl -sSL https://install.python-poetry.org | python -
    ```

2. **Activate the Virtual Environment:**
    Since this project `db_versions` has a virtual environment managed by Poetry, it can be activated using the following command:

    ```shell
    cd db_versions
    poetry shell
    ```

3. **Install Dependencies:**
    If the project's dependencies are not installed, the following command can be used to install them based on the pyproject.toml and poetry.lock files (under `db_versions`):

    ```shell
    poetry install
    ```

    To check the installed packages used in this Python project, check the file named `pyproject.toml`. For example: 
    ````
    [tool.poetry]
    name = "db-versions"
    version = "0.1.0"
    description = ""
    authors = ["feki-rihab <rihab.feki@fiware.org>"]
    readme = "README.md"

    [tool.poetry.dependencies]
    python = "^3.9"
    github-py = "^0.5.0"
    pymongo = "^4.6.1"
    pygithub = "^2.1.1"
    regex = "^2023.12.25"


    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    ````

4. **Add Dependencies (Optional):**
To customize this project or add more functionnalities to it, the `add` command can be used to add dependencies to it. 

    For example, to add the `requests` library, run:
    ```shell
    cd db_versions
    poetry add requests
    ```

5. **Run The Project:**
Once the virtual environment is activated, the Python script can be run using the `poetry run` command. 

    For example, to run a script named `main.py`, use:

    ```shell
    poetry run python main.py
    ````

# 






