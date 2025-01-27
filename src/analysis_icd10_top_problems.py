# analysis_icd10_top_problems.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from helpers.config import PLOTS_DIR, DATA_DIR, RESULTS_DIR
from helpers.utils import read_csv, write_excel
from helpers.matplotlib_utils import save_fig_matplotlib


def format_icd_labels(icd_codes, icd_names, max_length=50):
    formatted_labels = []
    for code, name in zip(icd_codes, icd_names):
        formatted_name = f"[{code}] {name}"
        if len(formatted_name) > max_length:
            formatted_name = formatted_name[: max_length - 3] + "..."
        formatted_labels.append(formatted_name)
    return formatted_labels


def analyze_icd10_top_problems():
    # Load the processed data
    file_path = (
        DATA_DIR / "processed" / "problemy_zdrowotne_icd10_poradnia_okulistyczna.csv"
    )
    df = read_csv(file_path)

    # Select relevant columns
    df = df[
        [
            "Rok",
            "Województwo",
            "Kod ICD-10 poziom 3.",
            "Nazwa ICD-10 poziom 3.",
            "Kod ICD-10 poziom 2.",
            "Nazwa ICD-10 poziom 2.",
            "Kod ICD-10 poziom 1.",
            "Nazwa ICD-10 poziom 1.",
            "Liczba porad AOS",
        ]
    ]

    # Set figure size based on A4 dimensions (in inches)
    fig_width = 11.7  # A4 width in inches (297mm)
    fig_height = 8.3  # Adjusted for horizontal layout

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(fig_width, fig_height))
    for idx, level in enumerate([1, 2, 3]):
        icd_code_col = f"Kod ICD-10 poziom {level}."
        icd_name_col = f"Nazwa ICD-10 poziom {level}."

        # Aggregate the number of consultations by ICD code
        top_icd = (
            df.groupby([icd_code_col, icd_name_col])["Liczba porad AOS"]
            .sum()
            .nlargest(10)
            .reset_index()
        )

        # Save data to Excel
        file_path = RESULTS_DIR / "icd10_top_problems_by_level.xlsx"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            write_excel(
                file_path=file_path,
                data=top_icd,
                sheet_name=f"Lvl_{level}",
                mode="w",
                index=False,
            )
        else:
            write_excel(
                file_path=file_path,
                data=top_icd,
                sheet_name=f"Lvl_{level}",
                mode="a",
                index=False,
            )

        formatted_labels = format_icd_labels(
            top_icd[icd_code_col], top_icd[icd_name_col]
        )

        # Plot the data
        bars = axes[idx].barh(
            formatted_labels, top_icd["Liczba porad AOS"], color="skyblue"
        )
        axes[idx].set_xlabel("Liczba porad AOS")
        axes[idx].set_title(f"Poziom {level}")
        axes[idx].invert_yaxis()

        # Adding values on the bars
        for bar in bars:
            width = bar.get_width()
            axes[idx].text(
                width + 500,
                bar.get_y() + bar.get_height() / 2,
                f"{int(width)}",
                ha="left",
                va="center",
                fontsize=8,
            )

    # Add a common title to the figure
    fig.suptitle(
        "Najczęstsze problemy zdrowotne (ICD-10)",
        fontsize=12,
        fontweight="normal",
        y=0.95,
    )

    # Add a common title to the y-axis
    fig.text(
        0.02, 0.5, "Kod ICD i Nazwa", va="center", rotation="vertical", fontsize=10
    )

    # Adjust layout to give more space to Y-axis labels
    plt.subplots_adjust(left=0.3, right=0.98, hspace=0.5)

    for ax in axes:
        ax.tick_params(axis="y", labelsize=8)
        ax.tick_params(axis="x", labelsize=8)

    # Save the combined figure
    save_fig_matplotlib(fig, PLOTS_DIR / "icd10_top_problems_all_levels.png")

    plt.close(fig)


if __name__ == "__main__":
    analyze_icd10_top_problems()
