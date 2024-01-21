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
    print("Starting data processing")
    result = {}
    for category, category_details in json_template.items():
        print(f"Processing category: {category}")
        cat_result = process_category(ini_data, category_details)
        if cat_result:
            result[category] = cat_result
    print("Processing completed")
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
            print(f"  Processing sub-category: {sub_category}")
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

    Args:
    ini_data (dict): Dictionary containing INI file data.
    sub_details (dict): Details of the sub-category to be processed.
    sub_category (str): Name of the sub-category.
    category_result (dict): Dictionary to store the results of processing.
    """
    tag = sub_details.get("tag", "").strip("[]")
    tags = sub_details.get("tags", [])
    if not tags and tag:
        tags = [tag]

    print(f"    Tags for {sub_category}: {tags}")

    entry = sub_details.get("entry")
    entries = sub_details.get("entries", {})
    return_value = sub_details.get("return_value", False)

    if not entries and not entry:
        # New logic to handle the absence of "entry" or "entries"
        if any(tag.strip("[]") in ini_data for tag in tags):
            print(f"    Tag found for {sub_category}, no specific entry required")
            category_result[sub_category] = True
        else:
            print(f"    Tag not found for {sub_category}")
        return

    if any(tag.strip("[]") in ini_data for tag in tags):
        print(f"    Tag found for {sub_category}")
        if check_entries(ini_data, tags, entries):
            if return_value and entry:
                for tag in tags:
                    tag = tag.strip("[]")
                    if tag in ini_data and entry in ini_data[tag]:
                        category_result[sub_category] = ini_data[tag].get(entry)
                        print(f"      Value returned for {sub_category}: {category_result[sub_category]}")
                        break
            else:
                category_result[sub_category] = True
        else:
            print(f"    Entries do not match for {sub_category}")
    else:
        print(f"    Tag not found for {sub_category}")

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
    print(f"Checking entries for tags: {tags}, with specific entries: {entries}")
    if not entries:
        # If no entries are specified, just check for the presence of tags
        for tag in tags:
            tag = tag.strip("[]")
            if tag in ini_data:
                print(f"Tag '{tag}' found without specific entries.")
                return True
        print("No matching tag found without specific entries.")
        return False

    # If entries are specified, check for the presence of the tag and matching of entries
    for tag in tags:
        tag = tag.strip("[]")
        if tag not in ini_data:
            print(f"Tag '{tag}' not found.")
            continue

        data = ini_data[tag]
        all_entries_match = True
        for key, value in entries.items():
            if value.endswith("!"):
                # For values ending with "!", check for inclusion
                search_value = value[:-1] # Remove "!" from the value
                if key not in data or search_value not in data[key]:
                    print(f"Entry '{key}' does not contain '{search_value}' for tag '{tag}'.")
                    all_entries_match = False
                    break
            else:
                # Exact match for other values
                if key not in data or data[key] != value:
                    print(f"Entry '{key}' does not match or is absent for tag '{tag}'.")
                    all_entries_match = False
                    break

        if all_entries_match:
            print(f"All specified entries match for tag '{tag}'.")
            return True

    print("No match for the specified tags and entries.")
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
