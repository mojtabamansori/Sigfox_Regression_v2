import json
import matplotlib.pyplot as plt
from function import *

file_path = '../Dataset/update/lorawan_antwerp_gateway_locations.json.txt'
gateway_matrix = parse_gateway_locations(file_path)
print(len(gateway_matrix))
latitudes = [row[1] for row in gateway_matrix]
longitudes = [row[2] for row in gateway_matrix]

