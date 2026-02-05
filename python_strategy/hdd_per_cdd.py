import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
# import requests
import matplotlib.colors as colors
import pandas as pd
import os
import numpy as np
from shapely import wkt

def plot_threshold_regions(all_data, parent_path):
    # discrete mapping
    #regime_names = {1: 'Cool Roof', 2: 'Green Roof'}
    #unique_regimes = sorted(all_data['roof_regime'].unique())
    
    # distinct colors
    colors_list = ["#cfcfcf", '#2ecc71']
    cmap = colors.ListedColormap(colors_list)

    fig, ax = plt.subplots(figsize=(20, 12))
    all_data.plot(
        column='roof_regime', 
        ax=ax, 
        cmap=cmap, 
        categorical=True, # Tells GeoPandas to treat values as categories
        legend=True,
        # legend_kwds for categorical data handles the labels automatically
        legend_kwds={'loc': 'lower right', 'title': "Roof Strategies"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("Recommended Roof Regime by US County", fontsize=20)
    
    # Save the map
    plt.savefig(parent_path / 'image/roof_regime_map.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_hdd_per_cdd(all_data, parent_path):
    # This makes 1.0 (equal heating/cooling) the center of your color map
    divnorm = colors.TwoSlopeNorm(vmin=0., vcenter=1., vmax=15.)

    fig, ax = plt.subplots(figsize=(10, 6))
    all_data.plot(
        column='HDD_per_CDD', 
        ax=ax, 
        cmap='RdYlBu_r', 
        norm=divnorm,
        legend=True,
        legend_kwds={'label': "2025 HDD per CDD", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("2025 HDD/CDD by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/hdd_per_cdd.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()

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

    # DO ANALYSIS
    all_data['HDD_per_CDD'] = all_data['HDD'] / all_data['CDD']

    all_data['CDD'].replace(0, np.nan)

    #create regimes
    #fake numbers
    all_data['roof_regime'] = all_data['HDD_per_CDD'] > 7

    # save data
    all_data.to_csv(parent_path / 'data/all_data.csv', index=False)

    # check data
    print("All Data HDD_per_CDD")
    print(all_data['HDD_per_CDD'].head())
    print("All Data HDD")
    print(all_data['HDD'].head())
    print("All Data CDD")
    print(all_data['CDD'].head())

    # Plot
    print('Plot HDD per CDD')
    plot_hdd_per_cdd(all_data, parent_path)
    print("Plot Regimes")
    plot_threshold_regions(all_data, parent_path)

if __name__ == "__main__":
    generate_map()