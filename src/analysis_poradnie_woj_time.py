# analysis_poradnie_woj_time.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel
from helpers.matplotlib_utils import save_fig_matplotlib, create_subplots_matplotlib


def analyze_clinics_by_region_time():
    """
    Analyzes the number of ophthalmology clinics in different regions over the years.
    Generates bar and line charts to visualize the trends.
    """
    # Load the processed data
    file_path = Path(DATA_DIR / "processed" / "swiad_woj_poradnia_okulistyczna.csv")
    df = read_csv(file_path)

    # Select relevant columns
    df = df[["Rok", "Województwo", "Liczba poradni AOS"]]

    # Create a pivot table for visualization
    pivot_table = df.pivot_table(
        index="Rok", columns="Województwo", values="Liczba poradni AOS", aggfunc="sum"
    )

    # Save pivot table to Excel
    file_path = Path(RESULTS_DIR / "clinics_by_region_time.xlsx")
    write_excel(file_path, pivot_table)

    # Define 16 distinct colors for województwa
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
        "#f5a742",
        "#a64d79",
        "#6a3d9a",
        "#ffb3e6",
        "#4daf4a",
        "#999999",
    ]

    # Plot Count Clinics by Region line chart using matplotlib
    fig, ax = create_subplots_matplotlib(n_plots=1, n_cols=1, figsize=(11.7, 8.3))
    ax = ax[0]
    pivot_table.plot(marker="o", ax=ax, color=colors)

    # Customize plot directly in code
    ax.set_xlabel("Rok")
    ax.set_ylabel("Liczba poradni")
    ax.grid(True)

    fig.suptitle(
        "Liczba poradni okulistycznych w województwach 2016-2023", fontsize=12, y=0.95
    )

    # Adjust layout to make space for legend
    fig.subplots_adjust(bottom=0.2)
    ax.get_legend().remove()
    fig.legend(
        labels=pivot_table.columns.tolist(),
        title=f"Województwo",
        loc="lower center",
        ncol=4,
    )

    # Save the figure
    save_fig_matplotlib(fig, Path(PLOTS_DIR) / "clinics_by_region_time.png")


if __name__ == "__main__":
    analyze_clinics_by_region_time()
