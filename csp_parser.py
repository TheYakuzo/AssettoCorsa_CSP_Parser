import json

def read_ini_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    ini_data = {}
    current_section = None

    for line in lines:
        line = line.strip()
        # Suppression des commentaires
        comment_index = line.find(';')
        if comment_index != -1:
            line = line[:comment_index].strip()

        # Continuez si la ligne est vide après suppression du commentaire
        if not line:
            continue

        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            ini_data[current_section] = {}
        elif '=' in line and current_section:
            key, value = line.split('=', 1)
            # Nettoyer la valeur (retirer les tabulations et les espaces supplémentaires)
            value = value.replace('\t', '').strip()
            ini_data[current_section][key.strip()] = value

    return ini_data


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def clean_value(value):
    """ Nettoie la valeur en enlevant les commentaires et les espaces superflus. """
    return value.split(';')[0].strip()

def process_data(ini_data, json_template):
    print("Début du traitement des données")
    result = {}
    for category, category_details in json_template.items():
        print(f"Traitement de la catégorie : {category}")
        cat_result = process_category(ini_data, category_details)
        if cat_result:
            result[category] = cat_result
    print("Traitement terminé")
    return result

def process_category(ini_data, category_details):
    category_result = {}

    # Gestion des sous-catégories
    if 'childs' in category_details:
        for sub_category, sub_details in category_details["childs"].items():
            print(f"  Traitement de la sous-catégorie : {sub_category}")
            if 'childs' in sub_details:
                sub_result = process_category(ini_data, sub_details)
                if sub_result:
                    category_result[sub_category] = sub_result
            else:
                process_sub_category(ini_data, sub_details, sub_category, category_result)
    else:
        # Vérifier directement les tags de la catégorie actuelle
        tag = category_details.get("tag", "").strip("[]")
        tags = category_details.get("tags", [])
        if not tags and tag:
            tags = [tag]

        # Si un tag est trouvé, assigner True à la catégorie
        if any(tag.strip("[]") in ini_data for tag in tags):
            return True

    return {k: v for k, v in category_result.items() if v}



def process_sub_category(ini_data, sub_details, sub_category, category_result):
    tag = sub_details.get("tag", "").strip("[]")
    tags = sub_details.get("tags", [])
    if not tags and tag:
        tags = [tag]

    print(f"    Tags pour {sub_category}: {tags}")

    entry = sub_details.get("entry")
    entries = sub_details.get("entries", {})
    return_value = sub_details.get("return_value", False)

    if not entries and not entry:
        # Nouvelle logique pour gérer l'absence de "entry" ou "entries"
        if any(tag.strip("[]") in ini_data for tag in tags):
            print(f"    Tag trouvé pour {sub_category}, aucune entrée spécifique nécessaire")
            category_result[sub_category] = True
        else:
            print(f"    Tag non trouvé pour {sub_category}")
        return

    if any(tag.strip("[]") in ini_data for tag in tags):
        print(f"    Tag trouvé pour {sub_category}")
        if check_entries(ini_data, tags, entries):
            if return_value and entry:
                for tag in tags:
                    tag = tag.strip("[]")
                    if tag in ini_data and entry in ini_data[tag]:
                        category_result[sub_category] = ini_data[tag].get(entry)
                        print(f"      Valeur retournée pour {sub_category}: {category_result[sub_category]}")
                        break
            else:
                category_result[sub_category] = True
        else:
            print(f"    Les entrées ne correspondent pas pour {sub_category}")
    else:
        print(f"    Tag non trouvé pour {sub_category}")

def check_entries(ini_data, tags, entries=None):
    print(f"Vérification des entrées pour les tags: {tags}, avec des entrées spécifiques: {entries}")
    if not entries:
        # Si aucune entrée n'est spécifiée, vérifiez uniquement la présence des tags
        for tag in tags:
            tag = tag.strip("[]")
            if tag in ini_data:
                print(f"Tag '{tag}' trouvé sans entrées spécifiques.")
                return True
        print("Aucun tag correspondant trouvé sans entrées spécifiques.")
        return False

    # Si des entrées sont spécifiées, vérifiez la présence du tag et la correspondance des entrées
    for tag in tags:
        tag = tag.strip("[]")
        if tag not in ini_data:
            print(f"Tag '{tag}' non trouvé.")
            continue

        data = ini_data[tag]
        all_entries_match = True
        for key, value in entries.items():
            if value.endswith("!"):
                # Pour les valeurs se terminant par "!", vérifier l'inclusion
                search_value = value[:-1] # Retirer le "!" de la valeur
                if key not in data or search_value not in data[key]:
                    print(f"L'entrée '{key}' ne contient pas '{search_value}' pour le tag '{tag}'.")
                    all_entries_match = False
                    break
            else:
                # Correspondance exacte pour les autres valeurs
                if key not in data or data[key] != value:
                    print(f"L'entrée '{key}' ne correspond pas ou est absente pour le tag '{tag}'.")
                    all_entries_match = False
                    break

        if all_entries_match:
            print(f"Toutes les entrées spécifiées correspondent pour le tag '{tag}'.")
            return True

    print("Aucune correspondance pour les tags et les entrées spécifiées.")
    return False



# For Cars
ini_file_path = './cars/ext_config.ini'
json_file_path = './cars/car_csp.json'
# For Tracks
# ini_file_path = './tracks/ext_config.ini'
# json_file_path = './tracks/track_csp.json'

ini_data = read_ini_file(ini_file_path)
json_template = read_json_file(json_file_path)

result = process_data(ini_data, json_template)
print(json.dumps(result, indent=4))
