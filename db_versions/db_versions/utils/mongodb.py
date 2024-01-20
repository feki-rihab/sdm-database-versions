import os
import json
from dotenv import load_dotenv
from github import Github
from pymongo import MongoClient


# Load environment variables from .env file
load_dotenv()


########################################################################
#                            connect to MongoDB                        #
########################################################################

def connect_to_mongodb(mongo_host, mongo_port, mongo_db_name, mongo_collection_name):
    """
    Connects to a MongoDB instance and retrieves a specific collection.

    Args:
    mongo_host (str): The host address of the MongoDB instance.
    mongo_port (int): The port number of the MongoDB instance.
    mongo_db_name (str): The name of the database to connect to.
    mongo_collection_name (str): The name of the collection to retrieve.

    Returns:
    pymongo.collection.Collection: The specified collection from the MongoDB database.
    """
    # Create a MongoDB client
    client = MongoClient(mongo_host, mongo_port)

    # get the database
    db = client[mongo_db_name]

    # get the collection
    collection = db[mongo_collection_name]

    return collection

########################################################################
#                          insert data in MongoDB                      #
########################################################################

def insert_data_mogodb(path_to_data: str, collection):
    """
    Insert data in MongoDB collection.

    This function takes a JSON file path and a MongoDB collection as input and inserts the data into the collection. If the data is a single document, it uses the `insert_one` method; otherwise, it uses the `insert_many` method.

    Parameters:
    - path_to_data (str): The path to the JSON file containing the data to be inserted.
    - collection (object): The MongoDB collection to insert the data into.

    Returns:
    - None
    """
    # Load data from versions.json
    with open(path_to_data, "r") as file:
        data = json.load(file)

    # Check if the data is a list and not empty
    if isinstance(data, list) and data:
        # Insert data into the MongoDB collection
        if len(data) == 1:
            result = collection.insert_one(data[0])
            print("Document inserted with the following ID:", result.inserted_id)
        else:
            result = collection.insert_many(data)
            print("Documents inserted with the following IDs:", result.inserted_ids)
    else:
        print("Data is not a non-empty list")


# Example usage

# Connection parameters
# MongoDB connection parameters - env variables 
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))

# Database and collection names
mongo_db_name = os.getenv("MONGO_DB_NAME")
collection = os.getenv("MONGO_COLLECTION_NAME")
path_to_data = "database_versions/database_versions/data/version_db.json"

insert_data_mogodb(path_to_data, collection)


########################################################################
#                    repopulate the databse of versions                #
########################################################################

# Insert the new version in the dataset 
# this function is called from the main.py 
# Gather all the exsiting versions from the dataset from Github and repopiulate the databse with accurate data 
# save this data in a json file here: data_path = "database_versions/database_versions/data/version_db.json"


def repopulate_database(repo_name, data_path, access_token):
    """
    Repopulate the database with the latest GitHub data.

    This function retrieves the latest commit information from the specified GitHub repository, 
    extracts the commit information, and inserts it into the MongoDB database.

    Parameters:
    - repo_name (str): The name of the GitHub repository.
    - data_path (str): The path to the JSON file where the commit information will be saved.
    - access_token (str): The GitHub access token.

    Returns:
    None
    """
    g = Github(access_token)

    # Get the repository
    repo = g.get_repo(repo_name)

    # Get the latest commit
    latest_commit = repo.get_commits()[0]

    # Extract the commit information
    commit_info = {
        "sha": latest_commit.sha,
        "message": latest_commit.commit.message,
        "author": latest_commit.commit.author.name,
        "date": latest_commit.commit.author.date.isoformat()
    }

    # Save the commit information to a JSON file
    with open(data_path, 'w') as file:
        json.dump(commit_info, file)

    # TODO: Update the database with the latest commit information
    # update the version 
        
    # Update the MongoDB database with the latest commit information
    # client = MongoClient(mongodb_uri)
    # db = client[database_name]
    # collection = db[collection_name]
    # collection.insert_one(commit_info)


# Example usage
#repo_name = "username/repository"
repo_name = 'smart-data-models/dataModel.Environment'
data_path = "database_versions/database_versions/data/version_db.json"

credentials = {
    "globalUser": os.getenv("GLOBAL_USER"),
    "token": os.getenv("TOKEN")
}

access_token = credentials["token"]


repopulate_database(repo_name, data_path, access_token)


########################################################################
#                             running code                             #
########################################################################

# Connection parameters
# MongoDB connection parameters - env variables 
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))

# Database and collection names
mongo_db_name = os.getenv("MONGO_DB_NAME")
mongo_collection_name = os.getenv("MONGO_COLLECTION_NAME")

# Connect to Mongodb and get the collection to insert the data to
collection = connect_to_mongodb(mongo_host, mongo_port, mongo_db_name, mongo_collection_name)

# Path to the json file that will be inserted in the mongodb collection  
data_path = "database_versions/database_versions/data/version_db.json"

insert_data_mogodb(path_to_data=data_path, collection=collection)
