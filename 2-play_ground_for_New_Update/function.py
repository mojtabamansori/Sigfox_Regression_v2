import numpy as np
import json


def parse_gateway_locations(file_path):
    """
    Parses a JSON file containing gateway locations and returns a matrix of gateway details.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A matrix where each row contains [key, latitude, longitude].
    """
    matrix = []

    try:
        # Read the file content
        with open(file_path, "r") as file:
            content = file.read().strip()
            # Parse JSON directly
            data = json.loads(content)
            # Process the data
            for key, value in data.items():
                matrix.append([key, value["latitude"], value["longitude"]])
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return matrix