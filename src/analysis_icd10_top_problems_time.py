# analysis_icd10_top_problems_time.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel
from helpers.matplotlib_utils import (
    save_fig_matplotlib,
    create_subplots_matplotlib,
)


def format_icd_labels(icd_codes, icd_names, max_length=50):
    formatted_labels = []
    for code, name in zip(icd_codes, icd_names):
        formatted_name = f"[{code}] {name}"
        if len(formatted_name) > max_length:
            formatted_name = formatted_name[: max_length - 3] + "..."
        formatted_labels.append(formatted_name)
    return formatted_labels


def analyze_icd10_by_year():
    """
    Analyzes the most common ICD-10 health issues at each classification level over the years.
    Generates bar and line charts to visualize the trends in percentages.
    """
    # Load the processed data
    file_path = Path(
        DATA_DIR / "processed" / "problemy_zdrowotne_icd10_poradnia_okulistyczna.csv"
    )
    df = read_csv(file_path)

    # Select relevant columns
    df = df[
        [
            "Rok",
            "Kod ICD-10 poziom 1.",
            "Nazwa ICD-10 poziom 1.",
            "Kod ICD-10 poziom 2.",
            "Nazwa ICD-10 poziom 2.",
            "Kod ICD-10 poziom 3.",
            "Nazwa ICD-10 poziom 3.",
            "Liczba porad AOS",
        ]
    ]

    for level in [1, 2, 3]:
        icd_code_col = f"Kod ICD-10 poziom {level}."
        icd_name_col = f"Nazwa ICD-10 poziom {level}."

        # Identify top 10 ICD-10 issues based on total number of consultations
        top_icd = (
            df.groupby([icd_code_col, icd_name_col])["Liczba porad AOS"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

        # Filter data for top 10 problems only
        df_filtered = df[df[icd_code_col].isin(top_icd[icd_code_col])]

        # Create a pivot table for visualization
        pivot_table = df_filtered.pivot_table(
            index="Rok", columns=icd_name_col, values="Liczba porad AOS", aggfunc="sum"
        )

        # Convert to percentages
        pivot_table_percentage = pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100

        # Format legend labels
        formatted_labels = format_icd_labels(
            top_icd[icd_code_col], top_icd[icd_name_col]
        )
        pivot_table_percentage.columns = formatted_labels

        # Save pivot table to Excel
        file_path = Path(RESULTS_DIR / f"icd10_top_problems_time.xlsx")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            write_excel(
                file_path,
                pivot_table_percentage,
                sheet_name=f"Lvl_{level}",
                mode="w",
                index=True,
            )
        else:
            write_excel(
                file_path,
                pivot_table_percentage,
                sheet_name=f"Lvl_{level}",
                mode="a",
                index=True,
            )

        # Plot trends over years
        fig, ax = create_subplots_matplotlib(n_plots=1, n_cols=1, figsize=(11.7, 8.3))
        ax = ax[0]
        pivot_table_percentage.plot(marker="o", ax=ax)

        ax.set_xlabel("Rok")
        ax.set_ylabel("Procentowy udział porad AOS")
        ax.grid(True, linestyle="--", alpha=0.7)

        fig.suptitle(
            f"Udział procentowy najczęstszych problemów zdrowotnych (ICD-10, poziom {level}) 2016-2023",
            fontsize=12,
            y=0.95,
        )

        # Adjust layout to make space for legend
        fig.subplots_adjust(bottom=0.2)
        ax.get_legend().remove()
        fig.legend(
            labels=formatted_labels,
            title=f"ICD-10 Poziom {level}",
            loc="lower center",
            ncol=2,
        )

        # Save the figure
        save_fig_matplotlib(
            fig, Path(PLOTS_DIR) / f"icd10_top_problems_lvl{level}_time.png"
        )


if __name__ == "__main__":
    analyze_icd10_by_year()
