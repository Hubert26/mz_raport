import pandas as pd
import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel, read_excel
from helpers.matplotlib_utils import create_subplots_matplotlib


def analyze_consultation_to_clinic_geo():
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

    # Load consultation statistics
    consultations_file = (
        DATA_DIR / "processed" / "statystyki_porad_poradnia_okulistyczna.csv"
    )
    df_consultations = read_csv(consultations_file)

    # Aggregate consultations by region
    df_consultations = df_consultations.groupby("Województwo", as_index=False)[
        "Liczba porad AOS"
    ].sum()

    # Convert the region names to lowercase to ensure consistency for merging
    df_clinics["Województwo"] = df_clinics["Województwo"].str.lower()
    df_consultations["Województwo"] = df_consultations["Województwo"].str.lower()

    # Merge clinic data with consultations data
    df_merged = df_clinics.merge(df_consultations, on="Województwo")

    # Calculate consultations per clinic
    df_merged["Consultations per clinic"] = (
        df_merged["Liczba porad AOS"] / 1000 / df_merged["Liczba poradni AOS"]
    )

    # Write results to an Excel file
    result_file_path = Path(
        RESULTS_DIR / "consultations_per_clinic_by_region_2023.xlsx"
    )
    write_excel(result_file_path, df_merged)

    # Merge with the map data
    map["JPT_NAZWA_"] = map["JPT_NAZWA_"].str.lower()
    map = map.merge(df_merged, left_on="JPT_NAZWA_", right_on="Województwo")

    # Create visualization
    fig, ax = create_subplots_matplotlib(1, 1, figsize=(12, 8))
    ax = ax[0]

    # Plot consultations per clinic
    map.plot(
        column="Consultations per clinic",
        cmap="PuBu",
        linewidth=0.8,
        edgecolor="black",
        legend=True,
        legend_kwds={
            "label": "Liczba porad AOS na poradnię (tys.)",
        },
        ax=ax,
    )
    ax.set_title("")
    ax.set_xticks([])
    ax.set_yticks([])

    # Save the figure
    plt.savefig(Path(PLOTS_DIR / "consultations_to_clinic_geo_2023.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    analyze_consultation_to_clinic_geo()
