
import json

def clean_mitre_data(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    cleaned_data = []

    for item in data.get('objects', []):
        if item.get('type') == 'attack-pattern':
            cleaned_item = {
                "id": item.get("id"),
                "name": item.get("name"),
                "description": item.get("description"),
                "kill_chain_phases": item.get("kill_chain_phases", []),
                "external_references": [
                    {
                        "source_name": ref.get("source_name"),
                        "url": ref.get("url"),
                        "external_id": ref.get("external_id")
                    }
                    for ref in item.get("external_references", [])
                ]
            }
            cleaned_data.append(cleaned_item)

    cleaned_data = [cleaned_data[0]]

    with open(output_file, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

    print(f"Cleaned data saved to {output_file}")

input_file = './local-files/mitre_attack_data.json'
output_file = './local-files/cleaned_mitre_attack_data_short.json'
clean_mitre_data(input_file, output_file)

