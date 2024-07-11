import utils
from prettytable import PrettyTable
import pandas as pd

# Read the CSV file
data = utils.get_df()

# Select relevant columns
selected_columns = ['type_equipement_ou_lieu', 'departement', 'n_departement', 'nombre_fauteuils_de_cinema']

# Filter the DataFrame to only include the relevant columns
data_selected = data[selected_columns].copy()

# Convert 'n_departement' to string to ensure proper sorting and clean NaN values
data_selected.loc[:, 'n_departement'] = data_selected['n_departement'].astype(str)
data_selected = data_selected.dropna(subset=['type_equipement_ou_lieu', 'n_departement', 'nombre_fauteuils_de_cinema'])

# Filter rows to include only cinemas and convert 'nombre_fauteuils_de_cinema' to numeric
data_cinema = data_selected[data_selected['type_equipement_ou_lieu'] == 'Cinéma'].copy()
data_cinema.loc[:, 'nombre_fauteuils_de_cinema'] = pd.to_numeric(data_cinema['nombre_fauteuils_de_cinema'], errors='coerce').fillna(0)

# Group by department number and sum the number of cinema seats
grouped_data = data_cinema.groupby('n_departement').agg({
    'nombre_fauteuils_de_cinema': 'sum',
    'departement': 'first'  # Use the first occurrence of the department name for display
}).reset_index()

# Sort the grouped data by region number (n_departement)
grouped_data_sorted = grouped_data.sort_values(by='n_departement')

# Use PrettyTable to display the grouped and summed data with orange tones
table = PrettyTable()

# Set the column names for PrettyTable with ANSI color codes for orange
table.field_names = [
    '\033[38;5;214mDepartement\033[0m', 
    '\033[38;5;214mN_Departement\033[0m', 
    '\033[38;5;214mTotal Cinema Seats\033[0m'
]

# Add rows to the table with ANSI color codes for orange
for index, row in grouped_data_sorted.iterrows():
    table.add_row([
        f'\033[38;5;214m{row["departement"]}\033[0m', 
        f'\033[38;5;214m{row["n_departement"]}\033[0m', 
        f'\033[38;5;214m{row["nombre_fauteuils_de_cinema"]}\033[0m'
    ])

# Print the table
print(table)
