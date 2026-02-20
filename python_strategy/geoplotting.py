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

def plot_min_temp(all_data, parent_path):
    divnorm = colors.TwoSlopeNorm(vmin=-30., vcenter=20., vmax=70.)

    fig, ax = plt.subplots(figsize=(10, 6))
    all_data.plot(
        column='MIN TEMP', 
        ax=ax, 
        cmap='RdYlBu_r', 
        norm=divnorm,
        legend=True,
        legend_kwds={'label': "2025 Minimum Temperature", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("2025 Minimum Temperature by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/min_temp.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 6))
    all_data.plot(
        column='MIN TEMP JAN', 
        ax=ax, 
        cmap='RdYlBu_r', 
        norm=divnorm,
        legend=True,
        legend_kwds={'label': "January 2025 Minimum Temperature", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("January 2025 Minimum Temperature by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/min_temp_jan.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()

def plot_max_temp(all_data, parent_path):
    divnorm = colors.TwoSlopeNorm(vmin=60., vcenter=90., vmax=120.)

    fig, ax = plt.subplots(figsize=(10, 6))
    all_data.plot(
        column='MAX TEMP', 
        ax=ax, 
        cmap='RdYlBu_r', 
        norm=divnorm,
        legend=True,
        legend_kwds={'label': "2025 Maximum Temperature", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("2025 Maximum Temperature by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/max_temp.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 6))
    all_data.plot(
        column='MAX TEMP JUL', 
        ax=ax, 
        cmap='RdYlBu_r', 
        norm=divnorm,
        legend=True,
        legend_kwds={'label': "July 2025 Maximum Temperature", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("July 2025 Maximum Temperature by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/max_temp_july.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()

    fig, ax = plt.subplots(figsize=(10, 6))
    all_data.plot(
        column='MAX TEMP AUG', 
        ax=ax, 
        cmap='RdYlBu_r', 
        norm=divnorm,
        legend=True,
        legend_kwds={'label': "August 2025 Maximum Temperature", 'orientation': "horizontal"},
        edgecolor='black', 
        linewidth=0.05
    )

    ax.set_axis_off()
    plt.title("August 2025 Maximum Temperature by County", fontsize=20)
    
    plt.savefig(parent_path / 'image/max_temp_aug.png', dpi=300, bbox_inches='tight')
    print("Map saved")
    plt.show()