# analysis_populacja_na_poradnie_geo.py
import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel, read_excel
from helpers.matplotlib_utils import create_subplots_matplotlib


def analyze_population_to_clinic_geo():
    # Load the shapefile containing the boundaries of Polish regions
    map = gpd.read_file(Path(DATA_DIR / "wojewodztwa.geojson"))

    # Load the processed data containing clinic information
    file_path = DATA_DIR / "processed" / "swiad_woj_poradnia_okulistyczna.csv"
    df_clinics = read_csv(file_path)

    # Select only relevant columns for analysis
    df_clinics = df_clinics[["Rok", "Województwo", "Liczba poradni AOS"]]

    # Filter the dataset to include only data from the latest full year (2023)
    df_clinics = df_clinics[df_clinics["Rok"] == 2023]

    # Aggregate the number of clinics by region (Województwo)
    df_clinics = (
        df_clinics.groupby("Województwo")["Liczba poradni AOS"].sum().reset_index()
    )

    # Load demographic data
    demography_file = DATA_DIR / "raw" / "demografia_wojewodztwa.csv"
    df_demography = read_csv(demography_file)

    # Filter dataset for the latest available year (2023)
    df_demography = df_demography[df_demography["Rok"] == 2023]

    # Select relevant columns for analysis
    df_clinics = df_clinics[["Województwo", "Liczba poradni AOS"]]
    df_demography = df_demography[["Województwo", "Liczba pacjentów"]]
    df_demography = df_demography.groupby("Województwo", as_index=False)[
        "Liczba pacjentów"
    ].sum()

    # Convert the region names to lowercase to ensure consistency for merging
    df_clinics["Województwo"] = df_clinics["Województwo"].str.lower()
    df_demography["Województwo"] = df_demography["Województwo"].str.lower()

    # Merge clinic data with population data
    df_merged = df_clinics.merge(df_demography, on="Województwo")

    # Calculate population to clinic
    df_merged["Population to clinic"] = (
        df_merged["Liczba pacjentów"] / 1000 / df_merged["Liczba poradni AOS"]
    )

    # Write results to an Excel file
    result_file_path = Path(RESULTS_DIR / "population_to_clinic_geo_2023.xlsx")
    write_excel(result_file_path, df_merged)

    # Merge with the map data
    map["JPT_NAZWA_"] = map["JPT_NAZWA_"].str.lower()
    map = map.merge(df_merged, left_on="JPT_NAZWA_", right_on="Województwo")

    # Create visualization
    fig, ax = create_subplots_matplotlib(1, 1, figsize=(12, 8))
    ax = ax[0]

    # Plot population to clinic
    map.plot(
        column="Population to clinic",
        cmap="PuBu",
        linewidth=0.8,
        edgecolor="black",
        legend=True,
        legend_kwds={
            "label": "Liczba pacjentów na poradnię (tys.)",
        },
        ax=ax,
    )

    ax.set_title("")
    ax.set_xticks([])
    ax.set_yticks([])

    # Save the figure
    plt.savefig(Path(PLOTS_DIR / "population_to_clinic_geo_2023.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    analyze_population_to_clinic_geo()
