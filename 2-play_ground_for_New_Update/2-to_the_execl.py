import json
import matplotlib.pyplot as plt
from function import *
import pandas as pd

file_path = '../Dataset/update/lorawan_antwerp_gateway_locations.json.txt'
gateway_matrix = parse_gateway_locations(file_path)
print(len(gateway_matrix))
idx = [row[0] for row in gateway_matrix]
latitudes = [row[1] for row in gateway_matrix]
longitudes = [row[2] for row in gateway_matrix]

gateway_data = {
    "Index": idx,
    "Latitude": latitudes,
    "Longitude": longitudes
}
gateway_df = pd.DataFrame(gateway_data)

# Save the DataFrame to a CSV file
file_name = "lorawan_antwerp_gateway_locations.csv"
gateway_df.to_csv(file_name, index=False)

print(f"Data has been saved to {file_name}")