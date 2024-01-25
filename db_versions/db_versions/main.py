########################################################################
#                            How to run this code                      #
########################################################################

# This code assumes that the monogodb databese is hosted locally.
# First, run the module "mongodb.py" to insert data in it. 
# Insert the https://smartdatamodels.org/extra/versions.json into the mongodb that you create locally.
# Before insertion, run the module under "data/update_version_json.py" to make the data ready for insertion. 

########################################################################
#                                 TO DOs                               #
########################################################################
# TODO
# make an addition that adds a column that describes the change from the commit msg 
# add column last update for the previous version 

########################################################################
#                                 Imports                              #
########################################################################
import os 

from dotenv import load_dotenv
from datetime import datetime

from db_versions.utils.utils import last_commit_date_url
from db_versions.utils.mongodb import connect_to_mongodb


# Load environment variables from .env file
load_dotenv()


########################################################################
#                     MongoDB version fetch and update                 #
########################################################################

def check_version_and_update(
    mongo_host, mongo_port, db_name, collection_name, subject, datamodel, version, last_commit_date
) -> str:
    """
    Checks the existence of a datamodel in the MongoDB database and compares the actual version to the 
    version given as input with the date of the last update. If the last commit date is newer, 
    the database is updated with the latest commit date and link to the version on GitHub.

    Args:
    mongo_host (str): The host address of the MongoDB instance.
    mongo_port (int): The port number of the MongoDB instance.
    db_name (str): The name of the database.
    collection_name (str): The name of the collection.
    subject (str): The subject of the datamodel.
    datamodel (str): The name of the datamodel.
    version (str): The version to compare.
    last_commit_date (str): The date of the last commit in ISO format (e.g., '2023-10-15T08:30:00Z').

    Returns:
    str: A message indicating the result of the operation.
    """
    # Connect to the MongoDB instance and get the collection
    collection = connect_to_mongodb(mongo_host, mongo_port, db_name, collection_name)
    
    # Query the database to fetch the datamodel by its name and subject
    existing_datamodel = collection.find_one({"subject": subject, "dataModel": datamodel})
    
    if existing_datamodel:
        # Compare the actual version to the version given as input with the date of the last update
        if existing_datamodel['version'] == version:
            last_update_date = datetime.strptime(existing_datamodel['date'], '%Y-%m-%dT%H:%M:%SZ')
            last_commit_date = datetime.strptime(last_commit_date, '%Y-%m-%dT%H:%M:%SZ')
            
            if last_commit_date > last_update_date:
                # Perform the update if the last commit date is newer
                collection.update_one({"subject": subject, "dataModel": datamodel}, {"$set": {"date": last_commit_date.isoformat()}})
                return "Database updated with the latest commit date"
            else:
                return "Database is already up to date"
        else:
            return "Input version does not match the actual version in the database"
    else:
        return "Datamodel not found in the database"


########################################################################
#                                 Run code                             #
######################################################################## 
if __name__ == "__main__":
    # Example usage of the check_version_and_update function

    # MongoDB connection parameters - env variables 
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = int(os.getenv("MONGO_PORT"))
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    mongo_collection_name = os.getenv("MONGO_COLLECTION_NAME")

    subject = "dataModel.AirQualityObserved"
    datamodel = "Environment"
    version = "0.0.1"
    search_string="$schemaVersion"

    # data should be compatible with the timestamp format from gitHub API 
    last_commit_date = '2023-10-15T08:30:00Z'

    #TODO: add an extra column about the update 
    # get the comment from the check version function 
    comment_about_commit = {"additional_info": "version update"}

    # Get the last commit date 
    file_path = "AirQualityObserved/schema.json"
    repo_name = 'smart-data-models/dataModel.Environment'
    # update this with repo_name = 'dataModel.Environment'

    access_token = os.getenv("PAT")

    result = last_commit_date_url(file_path, repo_name, access_token, search_string)
    if result is not None:
        # there is an update in schema.json
        last_commit_date, commit_url, sha = result
        # Further processing with the unpacked values
    else:
        # Handle the case where the result is None
        print("No commit data found in schema.json")

    # Check the version of the last commit and the database
    result_version = check_version_and_update(mongo_host, mongo_port, mongo_db_name, mongo_collection_name, subject, datamodel, version, last_commit_date)

    # Print the result
    print(result_version)

    