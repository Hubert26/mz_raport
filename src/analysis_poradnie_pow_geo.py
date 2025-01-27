# analysis_poradnie_woj_geo.py
import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
import os
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel
from helpers.matplotlib_utils import create_subplots_matplotlib


def analyze_clinics_by_county_geo():
    # Load the shapefile containing the boundaries of Polish regions
    powiaty = gpd.read_file(Path(DATA_DIR / "powiaty_mapped.geojson"))

    # Load the processed data containing clinic information
    file_path = DATA_DIR / "processed" / "swiad_pow_poradnia_okulistyczna.csv"
    df = read_csv(file_path)

    # Select only relevant columns for analysis
    df = df[["Rok", "Województwo", "Powiat", "Liczba poradni AOS"]]

    # Filter the dataset to include only data from the latest full year (2023)
    df = df[df["Rok"] == 2023]

    # Drop the "Rok" column as it is no longer needed
    df.drop(columns=["Rok"], inplace=True)

    df["Powiat"] = df["Powiat"].str.lower().str.strip()
    df["Województwo"] = df["Województwo"].str.lower().str.strip()
    df["full_name"] = df["Powiat"] + df["Województwo"].fillna("").apply(
        lambda x: f"_{x}" if x else ""
    )

    # Aggregate the number of clinics by region (Województwo)
    df_grouped = df.groupby(["full_name"])["Liczba poradni AOS"].sum().reset_index()

    # Write excel
    file_path = Path(RESULTS_DIR / "clinics_by_county_geo_2023.xlsx")
    write_excel(file_path, df_grouped)

    # Merge the clinic data with the map based on region names
    map = powiaty.merge(df_grouped, left_on="full_name", right_on="full_name")

    # Fill NaN values with 0 and assign back to the column
    map["Liczba poradni AOS"] = map["Liczba poradni AOS"].fillna(0)
    map["Liczba poradni AOS"] = map["Liczba poradni AOS"].astype(int)

    # Create a figure and axis using the utility function
    fig, ax = create_subplots_matplotlib(1, 1, figsize=(12, 8))
    ax = ax[0]

    # Plot the number of clinics by region using a choropleth map
    map.plot(
        column="Liczba poradni AOS",
        cmap="PuBu",
        linewidth=0.8,
        edgecolor="black",
        legend=True,
        ax=ax,
        missing_kwds={"color": "red", "edgecolor": "black", "hatch": "///"},
    )

    # Add a title to the plot
    ax.set_title("")

    # Remove axis ticks and labels for better visualization
    ax.set_xticks([])
    ax.set_yticks([])

    # Save the figure to a file
    file_path = Path(PLOTS_DIR / "clinics_by_county_geo_2023.png")
    if file_path.exists():
        os.remove(file_path)
    plt.savefig(file_path, dpi=300)
    plt.close()


if __name__ == "__main__":
    analyze_clinics_by_county_geo()
