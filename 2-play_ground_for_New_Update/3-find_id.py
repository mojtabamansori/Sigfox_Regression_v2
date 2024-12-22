import re

# Function to extract unique gateway IDs
def extract_unique_gateway_ids(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    # Regular expression to find gateway IDs
    gateway_ids = re.findall(r'"gateways": \[\{"id": "([A-Za-z0-9]+)"', content)
    # Return unique gateway IDs
    return list(set(gateway_ids))

# Specify the path to your .txt file
file_path = "../Dataset/update/lorawan_antwerp_2019_dataset.json.txt"

# Extract and print unique gateway IDs
unique_gateway_ids = extract_unique_gateway_ids(file_path)
print(len(unique_gateway_ids),"Extracted Unique Gateway IDs:", unique_gateway_ids)
