import json

def read_ini_file(file_path):
    """
    Reads a .ini file and returns its content as a dictionary.
    
    Args:
    file_path (str): The path to the .ini file.

    Returns:
    dict: A dictionary representation of the .ini file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    ini_data = {}
    current_section = None

    for line in lines:
        line = line.strip()
        # Remove comments from the line
        comment_index = line.find(';')
        if comment_index != -1:
            line = line[:comment_index].strip()

        # Skip if the line is empty after removing the comment
        if not line:
            continue

        # Detect and handle new sections
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            ini_data[current_section] = {}
        elif '=' in line and current_section:
            # Split the line into key and value and clean them
            key, value = line.split('=', 1)
            value = value.replace('\t', '').strip()
            ini_data[current_section][key.strip()] = value

    return ini_data



def read_json_file(file_path):
    """
    Reads a JSON file and returns its content.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    dict: A dictionary representation of the JSON file.
    """
    print(f"Lecture du fichier JSON : {file_path}")
    with open(file_path, 'r') as file:
        return json.load(file)
    
    

def process_data(ini_data, json_template):
    """
    Processes the INI data against the JSON template and extracts relevant information.

    Args:
    ini_data (dict): Dictionary containing INI file data.
    json_template (dict): JSON template for processing the data.

    Returns:
    dict: Extracted data based on the JSON template.
    """
    print("----------------------------------")
    print("----------------------------------")
    print(f"{ini_data}")
    print("----------------------------------")
    print("----------------------------------")
    result = {}
    for category, category_details in json_template.items():
        cat_result = process_category(ini_data, category_details)
        if cat_result:
            result[category] = cat_result
            
    return result



def process_category(ini_data, category_details):
    """
    Processes a single category of data based on the given details.

    Args:
    ini_data (dict): Dictionary containing INI file data.
    category_details (dict): Details of the category to be processed.

    Returns:
    dict: Result of processing the category.
    """
    category_result = {}

    # Handle sub-categories
    if 'childs' in category_details:
        for sub_category, sub_details in category_details["childs"].items():
            if 'childs' in sub_details:
                sub_result = process_category(ini_data, sub_details)
                if sub_result:
                    category_result[sub_category] = sub_result
            else:
                process_sub_category(ini_data, sub_details, sub_category, category_result)
    else:
        # Directly check the tags of the current category
        tag = category_details.get("tag", "").strip("[]")
        tags = category_details.get("tags", [])
        if not tags and tag:
            tags = [tag]

        # If a tag is found, assign True to the category
        if any(tag.strip("[]") in ini_data for tag in tags):
            return True

    return {k: v for k, v in category_result.items() if v}



def process_sub_category(ini_data, sub_details, sub_category, category_result):
    """
    Processes a sub-category of data based on the given details.
    """
    tag = sub_details.get("tag", "").strip("[]")
    tags = sub_details.get("tags", [])
    if not tags and tag:
        tags = [tag]

    foreach = sub_details.get("foreach", False)
    only_one = sub_details.get("only_one", False)
    
    if foreach:
        process_foreach_sub_category(ini_data, sub_details, sub_category, category_result, tags, only_one)
    else:
        process_single_sub_category(ini_data, sub_details, sub_category, category_result, tags)
        
        

def process_foreach_sub_category(ini_data, sub_details, sub_category, category_result, tags, only_one):
    """
    Processes a sub-category of data with 'foreach' logic.
    """
    found = False
    sub_category_result = {}

    if tags[0].endswith("..."):
        # Pour les tags avec '...'
        exact_tag = tags[0].strip("[].")
        index = 0
        for ini_tag in ini_data.keys():
            if ini_tag == exact_tag:
                if process_conditions(ini_data, sub_details, ini_tag, sub_category_result, index, only_one):
                    found = True
                    if only_one:
                        break
                index += 1
    else:
        # Pour les tags normaux avec indexation
        index = 0
        not_found_count = 0
        while not_found_count < 2:
            foreach_tag = tags[0].replace("_N", f"_{index}")
            if foreach_tag in ini_data:
                if process_conditions(ini_data, sub_details, foreach_tag, sub_category_result, index, only_one):
                    found = True
                    if only_one:
                        category_result[sub_category] = True
                        return  # Sortie immédiate si une condition est remplie et only_one est vrai
                not_found_count = 0
            else:
                not_found_count += 1
            index += 1

    if not only_one:
        category_result[sub_category] = sub_category_result
    elif not found:
        category_result[sub_category] = False



def process_single_sub_category(ini_data, sub_details, sub_category, category_result, tags):
    """
    Processes a single sub-category of data.
    """
    entry = sub_details.get("entry")
    entries = sub_details.get("entries", {})
    return_value = sub_details.get("return_value", False)
    
    # Vérifie si les conditions dans 'entries' sont remplies
    for tag in tags:
        tag = tag.strip("[]")
        if tag in ini_data:
            conditions_met = True
            if entries:
                for k, v in entries.items():
                    possible_values = v.split('|')
                    ini_value = ini_data[tag].get(k, None)
                    if not any(val.strip() == ini_value for val in possible_values):
                        conditions_met = False
                        break
            
            if conditions_met:
                if return_value and entry:
                    if isinstance(entry, list):
                        entry_values = {e.lower(): ini_data[tag].get(e, "") for e in entry}
                        category_result[sub_category] = entry_values
                    else:
                        entry_value = ini_data[tag].get(entry, "")
                        category_result[sub_category] = entry_value
                else:
                    category_result[sub_category] = True
                return  # Sort de la boucle dès qu'une condition est remplie


def process_conditions(ini_data, sub_details, tag, sub_category_result, index, only_one):
    """
    Processes conditions for a sub-category and updates the result.
    """
    entry = sub_details.get("entry")
    entries = sub_details.get("entries", {})
    return_value = sub_details.get("return_value", False)

    conditions_met = True
    if entries:
        for k, v in entries.items():
            possible_values = v.split('|')
            ini_value = ini_data[tag].get(k, None)
            if not any(val.strip() == ini_value for val in possible_values):
                conditions_met = False
                break

    if conditions_met:
        if return_value and entry:
            series_result = {e.lower(): ini_data[tag].get(e, "") for e in entry} if isinstance(entry, list) else ini_data[tag].get(entry, "")
            sub_category_result[str(index)] = series_result
        else:
            sub_category_result[str(index)] = True
        return True
    return False



def check_entries(ini_data, tags, entries=None):
    """
    Checks the entries for the specified tags.

    Args:
    ini_data (dict): Dictionary containing INI file data.
    tags (list): List of tags to check.
    entries (dict): Specific entries to check for each tag.

    Returns:
    bool: True if all specified entries match, False otherwise.
    """
    if not entries:
        # If no entries are specified, just check for the presence of tags
        for tag in tags:
            tag = tag.strip("[]")
            if tag in ini_data:
                return True
        return False

    # If entries are specified, check for the presence of the tag and matching of entries
    for tag in tags:
        tag = tag.strip("[]")
        if tag not in ini_data:
            continue

        data = ini_data[tag]
        all_entries_match = True
        for key, value in entries.items():
            if value.endswith("!"):
                # For values ending with "!", check for inclusion
                search_value = value[:-1] # Remove "!" from the value
                if key not in data or search_value not in data[key]:
                    all_entries_match = False
                    break
            elif '|' in value:
                # Split the value by '|' and check if any of the values is present
                possible_values = value.split('|')
                if key not in data or not any(val.strip() in data[key] for val in possible_values):
                    all_entries_match = False
                    break
            else:
                # Exact match for other values
                if key not in data or data[key] != value:
                    all_entries_match = False
                    break

        if all_entries_match:
            return True

    return False



# Paths for Cars and Tracks
ini_file_path = './cars/ext_config.ini'
json_file_path = './cars/car_csp.json'
# For Tracks
# ini_file_path = './tracks/ext_config.ini'
# json_file_path = './tracks/track_csp.json'

# Read and process the data
ini_data = read_ini_file(ini_file_path)
json_template = read_json_file(json_file_path)
result = process_data(ini_data, json_template)

# Print the results
print(json.dumps(result, indent=4))
