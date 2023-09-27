import json


def append_to_json_file(filename: str, json_content: dict) -> None:
    with open(filename, 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data.append(json_content)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
            
def get_last_posted_event(filename: str):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    try:
        return file_data[-1]
    except IndexError:
        return {"id": ""}
            
            
def list_posted_events(filename: str):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
    try:
        print(len(file_data))
        return file_data
    except IndexError:
        return [{"id": ""}]