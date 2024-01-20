# Python package: sdm-database-versions  
This package create a database of Smart Data Models versions in order to achieve functionalities like tracking the history of change in SDMs &amp; tracing the evolution of SDMs in every version upgrade.

# Create a Python Virtual Environement 

To create a virtual environment in Python using the `venv` module, the following command can be executed in the terminal:

```shell
python3 -m venv venv
```
To activate a virtual environment named "venv" in the root path, you can use the following command:

```shell
source venv/bin/activate
```

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

# Environment Variables 

To manage Environment Variables in this project, create a file `.env` in which you can define the needed variables that should be private and secrets e.g database credentials, access tokens, etc. For example: 

```yaml
MONGO_DB_NAME=your-database-name
MONGO_PORT=mongo-port
MONGO_HOST="127.0.0.1"
MONGO_COLLECTION_NAME=your-collection-name
TOKEN=github-token
```
Use the library `python-dotenv` to instantiate the env vars in the python modules, for example: 

```python
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection parameters - env variables 
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))
```













