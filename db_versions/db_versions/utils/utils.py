import json
import os
import requests
import time
from dotenv import load_dotenv
from github import Github
import re
from typing import Union, List, Dict


# Load environment variables from .env file
load_dotenv()

########################################################################
#                                json                                  #
########################################################################

def open_json(file_url):
    """
    Opens a json file or url
    """
    if file_url.startswith("http"):
        # it is a URL
        try:
            pointer = requests.get(file_url)
            return json.loads(pointer.content.decode('utf-8'))
        except:
            return None

    else:
        # it is a file
        try:
            file = open(file_url, "r")
            return json.loads(file.read())
        except:
            return None

########################################################################
#                         github rate for api calls                    #
######################################################################## 

def _github_rate(user, token, security_margin=2):
    """
    Check the remaining GitHub API calls for the authenticated user and wait if necessary.
    """
    try:
        # Get the current rate limit status
        response = requests.get('https://api.github.com/rate_limit', auth=(user, token))
        resonse_text = response.text
        response.raise_for_status()  # Raise an exception if the request fails
        rate_limit_data = response.json()

        # Extract rate limit information
        resources = rate_limit_data["resources"]["core"]
        remaining = resources["remaining"]  # Remaining API calls for the current window
        reset_time = resources["reset"]  # Timestamp when the rate limit resets
        used_calls = resources["used"]  # Number of API calls made in the current window

        # Calculate the time until the rate limit resets
        time_until_reset = reset_time - time.time()

        # Check if we're close to the rate limit
        if remaining < security_margin:
            # Calculate the pause time to wait until the rate limit resets
            pause_time = max(0, time_until_reset + 1)  # Add 1 second as a buffer
            print(f"Waiting for {pause_time:.2f} seconds until rate limit resets...")
            time.sleep(pause_time)

        # Print rate limit information
        print(f"Remaining API calls: {remaining}")
        print(f"Time until rate limit reset: {time_until_reset:.2f} seconds")
        print(f"Total API calls made in this window: {used_calls}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

########################################################################
#                         schema.json last commit                      #
########################################################################       

def last_commit_date_url(file_path: str, repo_name: str, access_token:str, search_string: str):
    """
    Retrieve the date of the last modification (commit) on a specific file within a GitHub repository and 
    check if the commit is related to the update of the schemaVersion key in the schema.json file.

    Parameters:
    - file_path (str): The path of the file to be checked (e.g., "WeatherForecast/schema.json").
    - repo_name (str): The name of the GitHub repository (e.g., "dataModel.Weather").
    - access_token (str): The GitHub personal access token for authentication.
    - search_string (str): The string to serach for in the commit file (e.g "schemaVersion")

    Returns:
    - list: A list containing the date of the last commit and the commit URL if the version key has been updated, sha , otherwise returns None.
    """

    # Replace 'your_access_token' with your personal access token
    g = Github(access_token)

    # Get the repository
    repo = g.get_repo(repo_name)

    # Get the file contents
    file = repo.get_contents(file_path)

    # Get the commits for the file
    commits = repo.get_commits(path=file_path)
    
    try:
    # Check if the schemaVersion key has been updated in the latest commit
        for commit in commits:
            if file.sha in commit.files:
                for file in commit.files:
                    if file.filename == file_path and search_string in file.changes:
                        return [commit.commit.author.date, commit.html_url, commit.sha]

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage:
file_path = "AirQualityObserved/schema.json"
repo_name = 'smart-data-models/dataModel.Environment'
search_string="$schemaVersion"
sha = "8f4639f06a2d5db8ba73a8983c276403a137d17c"

# credentials = {
#         "globalUser": os.getenv("GLOBAL_USER"),
#         "token": os.getenv("TOKEN")
#     }

# access_token = credentials["token"]
access_token = os.getenv("PAT")

result = last_commit_date_url(file_path, repo_name, access_token, search_string)

if result:
    commit_date, commit_url, sha = result
    print(f"Last Commit Date: {commit_date}")
    print(f"Commit URL: {commit_url}")
    print(f"Last commit sha: {sha}")


########################################################################
#                        Save_commit_data_to_file                      #
########################################################################

def extract_commit_data(repository_name:str, commit_sha: str, access_token: str, search_string:str) -> Union[List[Union[str, Dict[str, str]]], None]:
    """
    Extracts the schema version from a specific commit in a GitHub repository.

    Parameters:
    - repository_name (str): The name of the GitHub repository (e.g., "organization/repository").
    - commit_sha (str): The SHA of the commit for which information is to be extracted.
    - access_token (str): The GitHub personal access token for authentication.
    - search_string (str): The specific string to search for in the commit changes (e.g., "version key").
    
    Returns:
    - Union[List[Union[str, Dict[str, str]]], None]: A list containing the filename of the changed file, 
      the old version, and the new version if the search string is found, otherwise None.
    """ 

    # Initialize the Github instance
    g = Github(access_token)

    # Get the repository
    repo = g.get_repo(repository_name)

    # Check the remaining API calls and wait if necessary
    # the github_rate function is called to check the remaining API calls before making the repo.get_commit call. 
    # If the remaining API calls are close to the limit, the function will wait until the rate limit resets.
    _github_rate(repo, access_token)

    # Get the commit
    commit = repo.get_commit(sha=commit_sha) 

    # Extract the commit data
    commit_data = commit.raw_data

    # Check each file changed in the commit
    for file_changed in commit_data.get("files", []):
        if file_changed.get("filename") == file_path:
            # Check the specific changes made to the file
            # In the context of a GitHub commit, the "patch" represents the unified diff of the changes made to a file. 
            # A unified diff is a textual representation of the differences between two sets of lines in a file. 
            # It includes information about added lines, removed lines, and modified lines.
            patch = file_changed.get("patch")

            # Check if the version key has been updated in the schema.json file within the patch 
            if search_string in patch:     
                # Check if it the search_string exists twice 
                if patch.count(search_string) >= 2:    
                    # Find the index of the first occurrence of the search_string
                    first_index = patch.find(search_string)
                    # Find the index of the second occurrence of the search_string
                    second_index = patch.find(search_string, first_index + 1)
                else: 
                    print("version did not change")

                # Look for the version in the patch data 

                # Convert the line of the schema into a dict and then extract the value
                schema_line_old_version = patch[first_index:patch.find('\n', first_index)]
                schema_line_new_version = patch[second_index:patch.find('\n', second_index)]

                # Define the RegEx pattern
                pattern = r'\$(\w+)"\s*:\s*"([^"]+)"'

                # Extract the matches as a dictionary of the old version 
                matches_old_version = re.findall(pattern, schema_line_old_version)
                print(matches_old_version)
                old_version = {key: value for key, value in matches_old_version}

                # Extract the matches as a dictionary of the new version 
                matches_new_version = re.findall(pattern, schema_line_new_version)
                print(matches_new_version)
                new_version = {key: value for key, value in matches_new_version}

                # Output the result
                print(f" The old version is {old_version}")
                print(f" The new version is {new_version}")
                
                print(f"The {search_string} has changed in {file_changed.get('filename')} from {old_version} to {new_version}")

                # TODO: return the version only means the key 
                # 
                return [file_changed.get("filename"), old_version, new_version]
                      
        else:
            return None


# Example usage
# credentials = {
#         "globalUser": os.getenv("GLOBAL_USER"),
#         "token": os.getenv("TOKEN")
#     }

# access_token = credentials["token"]
        
repository_name = 'smart-data-models/dataModel.Environment'
access_token = os.getenv("PAT")
        
output_file = 'database_versions/database_versions/github_commit_data.json'
#commit_sha = last_commit_date_url(file_path, repo_name)[2]
commit_sha = "8f4639f06a2d5db8ba73a8983c276403a137d17c"

extract_commit_data(repository_name, commit_sha, access_token, search_string)


########################################################################
#                                 TODOs                                #
########################################################################
# TODO
# populte the database of versions 
# history of the changes 
# for every SDM I discover which commits are changing the schema.json and populate the database 
# from the function ectract_commit_url, I need to add data to the database 
# make sure to add the github rate before, not to exhaust the api, so that the program keeps on working 

# prepare THE MAIN function and extectue the whole code
