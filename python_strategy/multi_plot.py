import geoplotting as gplot
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.colors as colors
import pandas as pd
import os
import numpy as np
from shapely import wkt

def convert_geoid_data_to_number(temp_df, id_str):
    temp_df[id_str] = temp_df[id_str].apply(convert_geoid)
    return temp_df

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
def reformat_geodata(og_data, val_name):
    og_data = convert_geoid_data_to_number(og_data, "ID")
    og_data = og_data.loc[:, ['ID', 'Value']]
    og_data.rename(columns= {"Value" : val_name}, inplace=True)
    og_data.rename(columns= {"ID" : "GEOID"}, inplace=True)
    return og_data

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
    drought_path = parent_path / 'data/palmer_mod_drought_index_august.csv'
    drought_data = pd.read_csv(drought_path, skiprows=2)
    max_temp_june_path = parent_path / 'data/max_temp_june.csv'
    max_temp_june_data = pd.read_csv(max_temp_june_path, skiprows=3)
    max_temp_july_path = parent_path / 'data/max_temp_july.csv'
    max_temp_july_data = pd.read_csv(max_temp_july_path, skiprows=3)
    max_temp_august_path = parent_path / 'data/max_temp_august.csv'
    max_temp_august_data = pd.read_csv(max_temp_august_path, skiprows=3)
    min_temp_january_path = parent_path / 'data/min_temp_january.csv'
    min_temp_january_data = pd.read_csv(min_temp_january_path, skiprows=3)
    min_temp_february_path = parent_path / 'data/min_temp_february.csv'
    min_temp_february_data = pd.read_csv(min_temp_february_path, skiprows=3)
    min_temp_december_path = parent_path / 'data/min_temp_december.csv'
    min_temp_december_data = pd.read_csv(min_temp_december_path, skiprows=3)

    continental_path = parent_path / 'data/continental.csv'
    continental = pd.read_csv(continental_path)

    # Reformat data
    hdd_data = reformat_geodata(hdd_data, "HDD")
    cdd_data = reformat_geodata(cdd_data, "CDD")
    drought_data = reformat_geodata(drought_data, "PALMER MOD INDEX")
    max_temp_june_data = reformat_geodata(max_temp_june_data, "MAX TEMP JUN")
    max_temp_july_data = reformat_geodata(max_temp_july_data, "MAX TEMP JUL")
    max_temp_august_data = reformat_geodata(max_temp_august_data, "MAX TEMP AUG")
    min_temp_january_data = reformat_geodata(min_temp_january_data, "MIN TEMP JAN")
    min_temp_february_data = reformat_geodata(min_temp_february_data, "MIN TEMP FEB")
    min_temp_december_data = reformat_geodata(min_temp_december_data, "MIN TEMP DEC")

    # Merge similar datasets

    # Check head
    print("Printing Head of Continental")
    print(continental.head())

    # Merge with other datasets
    dd_data = hdd_data.merge(cdd_data, on='GEOID')
    dd_data = dd_data.merge(drought_data, on='GEOID')
    dd_data = dd_data.merge(max_temp_june_data, on='GEOID')
    dd_data = dd_data.merge(max_temp_july_data, on='GEOID')
    dd_data = dd_data.merge(max_temp_august_data, on='GEOID')
    dd_data = dd_data.merge(min_temp_january_data, on='GEOID')
    dd_data = dd_data.merge(min_temp_february_data, on='GEOID')
    dd_data = dd_data.merge(min_temp_december_data, on='GEOID')
    all_data = continental.merge(dd_data, on='GEOID')

    # 1. Convert the 'geometry' string column back into actual geometric objects
    all_data['geometry'] = all_data['geometry'].apply(wkt.loads)

    # 2. Convert the pandas DataFrame to a GeoDataFrame
    all_data = gpd.GeoDataFrame(all_data, geometry='geometry')

    # 3. Set the Coordinate Reference System (CRS) if known (optional but recommended)
    all_data.set_crs("EPSG:5070", inplace=True)

    # DO ANALYSIS

    # HDD per CDD
    all_data['CDD'].replace(0, np.nan)
    all_data['HDD_per_CDD'] = all_data['HDD'] / all_data['CDD']

    # Min temperature
    all_data['MIN TEMP'] = all_data[['MIN TEMP JAN', 'MIN TEMP FEB', 'MIN TEMP DEC']].min(axis=1)

    # Max temperature
    all_data['MAX TEMP'] = all_data[['MAX TEMP JUN', 'MAX TEMP JUL', 'MAX TEMP AUG']].max(axis=1)

    #create regimes
    #green roof
    all_data['GREEN ROOF'] = 0 # default value
    all_data.loc[all_data['MIN TEMP'] > 20, 'GREEN ROOF'] = 1
    all_data.loc[all_data['MIN TEMP'] > 31.3, 'GREEN ROOF'] = 2

    #cool roof
    all_data['COOL ROOF'] = (all_data['CDD'] > 2700) & (all_data['HDD'] < 3600) # based on >4 data

    # save data
    all_data.to_csv(parent_path / 'data/all_data.csv', index=False)

    # check data
    print("All Data HDD_per_CDD")
    print(all_data['HDD_per_CDD'].head())
    print("All Data HDD")
    print(all_data['HDD'].head())
    print("All Data CDD")
    print(all_data['CDD'].head())

    # PLOT EVERYTHING

    # plot HDD per CDD
    print('Plot HDD per CDD')
    #gplot.plot_hdd_per_cdd(all_data, parent_path)

    # plot thresholds
    print("Plot Regimes")
    gplot.plot_green_roof_regime(all_data, parent_path)
    gplot.plot_cool_roof_regime(all_data, parent_path)

    # plot min temperatures
    print('Plot MIN TEMP')
    #gplot.plot_min_temp(all_data, parent_path)

    # plot max temperatures
    print('Plot MAX TEMP')
    #gplot.plot_max_temp(all_data, parent_path)

if __name__ == "__main__":
    generate_map()