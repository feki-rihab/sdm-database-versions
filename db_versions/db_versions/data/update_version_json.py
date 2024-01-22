import json


def remove_id_from_json_file(file_path, new_file_path):
    """
    Remove the "_id" field from a JSON file.
    Args:
    - file_path: The path to the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Remove the "_id" field from each dictionary in the JSON data
    for item in data:
        item.pop('_id', None)

    # Write the modified data back to the file
    with open(new_file_path, 'w') as file:
        json.dump(data, file, indent=2)


# Example usage
remove_id_from_json_file('versions.json', 'versions_db.json')