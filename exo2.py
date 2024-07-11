import utils
import pandas as pd
import matplotlib.pyplot as plt

# Debugging: Print a message
print("Python so sloooooooooooooooooooooooooooooooooooooooooow")

# Get the data from the CSV file
data = utils.get_df()

# Debugging: Print initial columns
print("Initial columns:", data.columns)

# Merge duplicate columns by combining their data
data = data.groupby(level=0, axis=1).first()

# Debugging: Print columns after removing duplicates
print("Columns after merging duplicates:", data.columns)

# Ensure 'region' column exists
if 'region' not in data.columns:
    raise ValueError("The 'region' column is not present in the data")

# Select and clean the necessary data
selected_columns = ['region']
data_selected = data[selected_columns].dropna()

# Normalize region names to handle case sensitivity and common typos
data_selected['region'] = data_selected['region'].str.strip().str.lower().str.title()

# Mapping for correcting common variations and typos in region names
region_corrections = {
    "Auverge-Rhône-Alpes": "Auvergne-Rhône-Alpes",
    "Ile-De-France": "Île-De-France",
    # Add other corrections as needed
}

data_selected['region'] = data_selected['region'].replace(region_corrections)

# Group the data by region and count the number of BaLEC
region_counts = data_selected['region'].value_counts().sort_index()

# Debugging: Print the region counts
print("Region counts:", region_counts)

# Set up Matplotlib style
plt.style.use('dark_background')

# Create the bar plot
fig, ax = plt.subplots(figsize=(14, 8))
bars = ax.bar(region_counts.index, region_counts.values, color='orange', edgecolor='white')

# Add title and axis labels
ax.set_title('Nombre de BaLEC par région', fontsize=20, fontweight='bold', color='white')
ax.set_xlabel('Région', fontsize=16, color='white')
ax.set_ylabel('Nombre de BaLEC', fontsize=16, color='white')
ax.set_xticklabels(region_counts.index, rotation=45, ha='right', fontsize=12, color='white')

# Add labels to bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=12, fontweight='bold', color='white')

# Add grid for better readability
ax.yaxis.grid(True, color='gray')
ax.xaxis.grid(False)

# Add margin to avoid cutting off labels
plt.tight_layout()

# Show the plot
plt.show()
