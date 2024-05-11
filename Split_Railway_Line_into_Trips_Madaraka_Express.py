#Created by David Straughan
#11/05/2024

import os
import pandas as pd

# Define stations and their exact coordinates
stations = [
    ("Mombasa Terminus", 39.57953978037501, -4.02110149656832),
    ("Mariakani SGR Station", 39.4605304999579, -3.860465702986496),
    ("Miasenyi SGR Station", 38.92177639733693, -3.657374309347545),
    ("Voi SGR Station", 38.55698879470904, -3.403804894425063),
    ("Mtito Andei SGR Station", 38.17126915010022, -2.690455946747341),
    ("Kibwezi SGR Station", 37.93706557614189, -2.406514699339472),
    ("Emali SGR Station", 37.47263179539603, -2.083976402116318),
    ("Athi River SGR Station", 36.99360022226065, -1.460459477798166),
    ("Nairobi Terminus", 36.89771239356276, -1.355204004817686)
]

# Function to read coordinates from a file
def read_coordinates(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace(')', '').replace('(', '')
        lines = content.split(',')
        coordinates = [(float(line.split()[0]), float(line.split()[1])) for line in lines if line.strip()]
    return coordinates

# Read the coordinates from the file
coordinates = read_coordinates('C:/Users/Admin/OneDrive/Desktop/FIG Project/Reversed_Coordinates.txt')

# Create output directory
output_dir = "C:/Users/Admin/OneDrive/Desktop/FIG Project/Station Trips"
os.makedirs(output_dir, exist_ok=True)

# Function to generate all paths
def generate_all_paths(coordinates, stations, output_dir):
    # Function to find the index of a station's coordinates in the full list, with tolerance for slight differences
    def find_coordinate_index(station_coordinates):
        tolerance = 0.0001
        for index, coord in enumerate(coordinates):
            if (abs(coord[0] - station_coordinates[0]) <= tolerance and abs(coord[1] - station_coordinates[1]) <= tolerance):
                return index
        return None

    # Iterate over all pairs of stations to create path files
    for i, (start_station, start_lat, start_lon) in enumerate(stations):
        start_index = find_coordinate_index((start_lat, start_lon))
        if start_index is None:
            continue  # Skip if start index is not found

        for j, (end_station, end_lat, end_lon) in enumerate(stations):
            if i != j:  # Ensure not the same station
                end_index = find_coordinate_index((end_lat, end_lon))
                if end_index is None:
                    continue  # Skip if end index is not found

                # Determine the slice of coordinates based on index positions
                path_coordinates = coordinates[min(start_index, end_index):max(start_index, end_index) + 1]
                if start_index > end_index:
                    path_coordinates = path_coordinates[::-1]  # Reverse if necessary

                # Construct file path and write coordinates to file
                filename = f"{start_station.replace(' ', '_')}_to_{end_station.replace(' ', '_')}.txt"
                with open(os.path.join(output_dir, filename), 'w') as file:
                    for coord in path_coordinates:
                        file.write(f"{coord[0]}, {coord[1]}\n")

# Call function to generate all paths
generate_all_paths(coordinates, stations, output_dir)


def correct_columns_and_swap(directory):
    # Loop over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            # Read the file, assuming current format without headers
            df = pd.read_csv(file_path, header=None, names=['Longitude', 'Latitude'])
            # Swap the columns back to the correct order
            df = df[['Latitude', 'Longitude']]
            # Save the DataFrame back to the file with column headings
            df.to_csv(file_path, index=False, header=True)

# Directory containing the files
directory = "C:/Users/Admin/OneDrive/Desktop/FIG Project/Station Trips"

# Call the function to swap columns back and ensure the headers are correct
correct_columns_and_swap(directory)

# Output message
print("Files have been updated to have the correct column order with 'Latitude' and 'Longitude' as headings.")
