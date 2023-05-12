import json

# Define your input file containing a list of JSON objects
input_file = 'path/to/your/input_file.jsonl'

# Define the output schema file
output_schema_file = 'json_schema.json'

# Function to update the schema with the data from the given JSON object
def update_schema_with_object(schema, json_obj):
    for key, value in json_obj.items():
        if key not in schema:
            if isinstance(value, dict):
                schema[key] = {
                    "type": "object",
                    "properties": update_schema_with_object({}, value)
                }
            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                schema[key] = {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": update_schema_with_object({}, value[0])
                    }
                }
            else:
                schema[key] = {
                    "type": type(value).__name__,
                    "example": value
                }
        elif schema[key]["type"] == "object" and isinstance(value, dict):
            schema[key]["properties"] = update_schema_with_object(schema[key]["properties"], value)
        elif schema[key]["type"] == "array" and isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            schema[key]["items"]["properties"] = update_schema_with_object(schema[key]["items"]["properties"], value[0])

    return schema

# Generate the JSON schema
def generate_json_schema(input_file):
    schema = {}
    with open(input_file, 'r') as file:
        for line in file:
            json_obj = json.loads(line.strip())
            schema = update_schema_with_object(schema, json_obj)
    return schema

# Run the script and generate the JSON schema
json_schema = generate_json_schema(input_file)

# Write the JSON schema to a file
with open(output_schema_file, 'w') as outfile:
    json.dump(json_schema, outfile, indent=4)
