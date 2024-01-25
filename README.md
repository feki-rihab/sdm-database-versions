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


# Connect to MongoDB via the Terminal

This project aims to create a database of versions for the Smart Data Models. To achieve this, interaction with the `smartdatamodels` database in MongoDB is essential. It's important to note that the MongoDB database is hosted in a virtual machine, and the code interacts with it.

## Create a MongoDB database locally 

Since, it is not possible to access the MongoDB database hosted in the virtual machine. A solution is to create a local MongoDB database that simulated the database hosted in the VM. 

To connect to MongoDB via the terminal, follow these steps:

1. Install MongoDB: Visit the [official MongoDB download website](https://www.mongodb.com/download-center/community/releases) and download the version for your specific operating system

1. Open the terminal 

2. Launch the MongoDB shell by running the command:
    ```
    mongosh
    ```

3. Switch to the `smartdatamodels` database by executing:

    ```shell
    use smartdatamodels
    ```

4. Display the collections in the current database:
    ````
    show collections
    ````
5. Query a specific collection. 
For example, to retrieve a document from the versions collection, run:

    ```shell
    db.versions.findOne()
    ```

    Here's an example of the output you might see after running the db.versions.findOne() command:

    ```json
    {
    _id: ObjectId("object_ID"),
    subject: 'dataModel.User',
    dataModel: 'Activity',
    version: '0.1.1',
    link: 'https://api.github.com/repos/smart-data-models/dataModel.User/git/commits/sha',
    date: '2022-09-06T07:29:54Z',
    publicLink: 'https://github.com/smart-data-models/dataModel.User/commit/sha'
    }
    ```
    This output represents a document from the `versions` collection in the smartdatamodels database.

## MongoDB Data 
To be able to run this code, it is needed to host a MongoDB database and insert the approprite data (e.g data under `db_versions/data/versions.json`) in it, to do that, the module `db_versions/utils/mongodb.py` is used to acheive that. 

```shell
Python3 mongodb.py
```

# Running the code 

To execute the main logic, it only takes to run the following command:

```shell
python3 main.py
```

The ruslt should look like this (as an example):

```
The old version is {'schemaVersion': '0.1.2'}
The new version is {'schemaVersion': '0.1.3'}
The $schemaVersion has changed in AirQualityObserved/schema.json from {'schemaVersion': '0.1.2'} to {'schemaVersion': '0.1.3'}
```