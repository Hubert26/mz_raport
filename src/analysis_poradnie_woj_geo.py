# analysis_poradnie_woj_geo.py
import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel
from helpers.matplotlib_utils import create_subplots_matplotlib


def analyze_clinics_by_region_geo():
    # Load the shapefile containing the boundaries of Polish regions
    map = gpd.read_file(Path(DATA_DIR / "wojewodztwa.geojson"))

    # Load the processed data containing clinic information
    file_path = DATA_DIR / "processed" / "swiad_woj_poradnia_okulistyczna.csv"
    df = read_csv(file_path)

    # Select only relevant columns for analysis
    df = df[["Rok", "Województwo", "Liczba poradni AOS"]]

    # Filter the dataset to include only data from the latest full year (2023)
    df = df[df["Rok"] == 2023]

    # Drop the "Rok" column as it is no longer needed
    df.drop(columns=["Rok"], inplace=True)

    # Aggregate the number of clinics by region (Województwo)
    df_grouped = df.groupby("Województwo")["Liczba poradni AOS"].sum().reset_index()

    # Write excel
    file_path = Path(RESULTS_DIR / "clinics_by_region_geo_2023.xlsx")
    write_excel(file_path, df_grouped)

    # Convert the region names to lowercase to ensure consistency for merging
    map["JPT_NAZWA_"] = map["JPT_NAZWA_"].str.lower()
    df_grouped["Województwo"] = df_grouped["Województwo"].str.lower()

    # Merge the clinic data with the map based on region names
    map = map.merge(df_grouped, left_on="JPT_NAZWA_", right_on="Województwo")

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
    )

    # Add a title to the plot
    ax.set_title("")

    # Remove axis ticks and labels for better visualization
    ax.set_xticks([])
    ax.set_yticks([])

    # Save the figure to a file
    plt.savefig(Path(PLOTS_DIR / "clinics_by_region_geo_2023.png"), dpi=300)
    plt.close()


if __name__ == "__main__":
    analyze_clinics_by_region_geo()
