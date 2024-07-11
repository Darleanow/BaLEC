import sys
import os
import pandas as pd
import folium
import random

def generate_pastel_color():
    """Generates a random pastel color."""
    r = lambda: random.randint(100, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

def generate_map(department_number):
    # Read the CSV file containing cultural equipment data
    data = pd.read_csv('base-des-lieux-et-des-equipements-culturels.csv', delimiter=';', header=0, low_memory=False)

    # Filter the data for the specified department and 'Monument' type
    filtered_data = data[(data['n_departement'] == str(department_number)) & 
                         (data['type_equipement_ou_lieu'] == 'Monument')]

    # Filter rows with valid GPS coordinates
    filtered_data = filtered_data.dropna(subset=['coordonnees_gps_lat_lon'])

    # Extract GPS coordinates, names, and types of monuments
    lats, lons, names, types = [], [], [], []
    for _, row in filtered_data.iterrows():
        try:
            lat, lon = map(float, row['coordonnees_gps_lat_lon'].split(','))
            lats.append(lat)
            lons.append(lon)
            # Clean the monument names to remove quotes
            name = row['nom'].replace('"', '').replace("'", "")
            names.append(name)
            # Add the type of monument
            monument_type = row['label_et_appellation']
            types.append(monument_type)
        except ValueError:
            continue

    # If no data is found
    if not lats or not lons:
        print("No monument found for this department.")
        return

    # Initialize the map with folium and a dark theme
    map_center = [sum(lats) / len(lats), sum(lons) / len(lons)]  # Center on the average coordinates of the department
    map_ = folium.Map(location=map_center, zoom_start=10, tiles='cartodb dark_matter')

    # Define marker colors based on the type of monument
    type_colors = {}
    for monument_type in set(types):
        type_colors[monument_type] = generate_pastel_color()

    # Add markers with customized infoboxes
    for lat, lon, name, monument_type in zip(lats, lons, names, types):
        marker_color = type_colors.get(monument_type, 'red')
        popup_content = f"""
        <div style="background-color: #212529; color: {marker_color}; font-weight: bold; padding: 5px;">{name}</div>
        """
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.DivIcon(html=f"""
            <div style="
                background-color: {marker_color};
                border: 2px solid white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;">
                <div style="
                    background-color: {marker_color};
                    border: 2px solid {marker_color};
                    border-radius: 50%;
                    width: 12px;
                    height: 12px;">
                </div>
            </div>
            """)
        ).add_to(map_)

    # Add the legend in a dark theme
    legend_html = '<div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: auto; background-color: #212529; color: white; z-index:9999; font-size:14px; border:2px solid grey; padding: 10px;">'
    legend_html += '<b>Legend:</b><br>'
    for monument_type, color in type_colors.items():
        legend_html += f'<i class="fa fa-map-marker" style="color:{color}"></i> {monument_type}<br>'
    legend_html += '</div>'
    map_.get_root().html.add_child(folium.Element(legend_html))

    # Define the output directory and file name
    output_dir = f"generated/{department_number}"
    output_file = f"monuments_department_{department_number}.html"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    # Save the map as HTML
    map_.save(output_path)
    print(f"Map generated: {output_path}")

    # Add custom CSS and script to style the popups
    add_custom_css_script(output_path)

def add_custom_css_script(html_file):
    """Adds custom CSS and script to style the popups."""
    custom_css_script = """
    <style>
        .leaflet-popup-content-wrapper {
            background-color: #212529;
            color: white;
            font-weight: bold;
        }
        .leaflet-popup-tip {
            background-color: #212529;
        }
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var map = L.map('map').setView([46.603354, 1.888334], 5);
            var targetLatLng = map.getCenter();
            setTimeout(function() {
                map.setView(targetLatLng, 10, {animate: true});
            }, 1000);
        });
    </script>
    """
    with open(html_file, 'r') as file:
        content = file.read()
    
    content = content.replace('</body>', custom_css_script + '</body>')

    with open(html_file, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python exo3.py <Department number>")
        sys.exit(1)

    department_number = sys.argv[1]
    generate_map(department_number)
