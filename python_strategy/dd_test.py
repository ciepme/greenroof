import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import requests
import pandas as pd
import os
from shapely import wkt

def convert_geoid_data_to_number(temp_df, id_str):
    temp_df[id_str] = temp_df[id_str].apply(convert_geoid)
    return temp_df # MUST return the dataframe

def convert_geoid(geoid_str):
    """
    Converts GeoID from 'LL###' (e.g., 'AL001') to '#####' (e.g., '01001').
    """
    state_to_fips = {
        'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08',
        'CT': '09', 'DE': '10', 'FL': '12', 'GA': '13', 'HI': '15', 'ID': '16',
        'IL': '17', 'IN': '18', 'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22',
        'ME': '23', 'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28',
        'MO': '29', 'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 'NJ': '34',
        'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39', 'OK': '40',
        'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46', 'TN': '47',
        'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54',
        'WI': '55', 'WY': '56', 'DC': '11'
    }

    # Extract the parts
    letters = geoid_str[:2].upper()  # Get LL
    numbers = geoid_str[3:]          # Get ###

    # Look up the state code
    state_code = state_to_fips.get(letters)

    if state_code:
        # Return state code + the 3-digit county code padded with zeros
        return int(f"{state_code}{numbers.zfill(3)}")
    else:
        return None # Or return the original if no match found

def generate_map():
    os.chdir('C:/Users/ciepm/OneDrive/Documents/Github/greenroof/python_strategy')
    pwd = os.getcwd()
    print("PWD is " + pwd)

    # Get NOAA Data
    parent_path = Path(pwd).parent
    print("Parent path is " + str(parent_path))
    hdd_path = parent_path / 'data/hdd_with_meta.csv'
    hdd_data = pd.read_csv(hdd_path, skiprows=3)
    cdd_path = parent_path / 'data/cdd_with_meta.csv'
    cdd_data = pd.read_csv(cdd_path, skiprows=3)
    continental_path = parent_path / 'data/continental.csv'
    continental = pd.read_csv(continental_path)

    # Reformat data
    hdd_data = convert_geoid_data_to_number(hdd_data, "ID")
    hdd_data.rename(columns= {"Value" : "HDD"}, inplace=True)
    hdd_data.rename(columns= {"ID" : "GEOID"}, inplace=True)
    cdd_data = convert_geoid_data_to_number(cdd_data, "ID")
    cdd_data.rename(columns= {"Value" : "CDD"}, inplace=True)
    cdd_data.rename(columns= {"ID" : "GEOID"}, inplace=True)

    # Check head
    print("Printing Head of HDD")
    print(hdd_data.head())
    print("Printing Head of CDD")
    print(cdd_data.head())
    print("Printing Head of Continental")
    print(continental.head())

    # Merge with other datasets
    dd_data = hdd_data.merge(cdd_data, on='GEOID')
    all_data = continental.merge(dd_data, on='GEOID')

    # 1. Convert the 'geometry' string column back into actual geometric objects
    all_data['geometry'] = all_data['geometry'].apply(wkt.loads)

    # 2. Convert the pandas DataFrame to a GeoDataFrame
    all_data = gpd.GeoDataFrame(all_data, geometry='geometry')

    # 3. Set the Coordinate Reference System (CRS) if known (optional but recommended)
    all_data.set_crs("EPSG:5070", inplace=True) 

    # 4. Now the plot call will work correctly
    fig, ax = plt.subplots(figsize=(20, 12))
    all_data.plot(
        column='HDD', 
        ax=ax, 
        cmap='RdYlBu_r', 
        legend=True,
        legend_kwds={'label': "2025 HDD", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("2025 HDD by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/hdd.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()

if __name__ == "__main__":
    generate_map()