# mz_raport

This project is part of a recruitment task for the Ministry of Health, aiming to create a synthetic report on health issues reported by patients within ophthalmology outpatient clinics. The report will analyze the state of ophthalmology clinics, including the number of facilities and the volume of provided healthcare services related to various health problems of patients. A crucial aspect of the report is to capture the temporal variability of observed phenomena.

The report is intended for management purposes, with the Minister of Health as the primary audience.

## Project Structure

```
mz_raport/
│-- data/                          # Directory containing project data
│   ├── raw/                        # Raw data files before processing
│   ├── processed/                   # Processed data after cleaning and EDA
│       ├── problemy_zdrowotne_icd10_poradnia_okulistyczna.csv   # Health issues based on ICD-10 classification for ophthalmology clinics
│       ├── statystyki_porad_poradnia_okulistyczna.csv           # Statistics on medical consultations in ophthalmology clinics
│       ├── statystyki_zakresow_produktow_poradnia_okulistyczna.csv  # Statistics on the range of products in ophthalmology clinics
│       ├── swiad_pow_poradnia_okulistyczna.csv                  # Outpatient services data at county level
│       ├── swiad_woj_poradnia_okulistyczna.csv                  # Outpatient services data at regional level
│       ├── teleporady_poradnia_okulistyczna.csv                  # Data on teleconsultations in ophthalmology clinics
│-- notebooks/                   # Jupyter notebooks for exploratory data analysis (EDA)
│   ├── eda_demografia_powiaty.ipynb            # EDA on county-level demographics
│   ├── eda_demografia_wojewodztwa.ipynb         # EDA on regional-level demographics
│   ├── eda_problemy_zdrowotne_icd10.ipynb       # EDA on health issues by ICD-10 classification
│   ├── eda_statystyki_porad.ipynb               # EDA on consultation statistics
│   ├── eda_statystyki_zakresow_produktow.ipynb   # EDA on service range statistics
│   ├── eda_swiad_pow.ipynb                       # EDA on outpatient services by county
│   ├── eda_swiad_woj.ipynb                       # EDA on outpatient services by region
│   ├── eda_teleporady.ipynb                       # EDA on teleconsultations
│-- plots/                     # Generated visualization files
│-- results/                    # Output results, reports, and analysis summaries
│-- src/                        # Source code
│   ├── __init__.py                # Initializes the src directory as a Python package
│   ├── main.py                    # Entry point for the project
│   ├── analysis_icd10_top_problems_time.py       # Analysis of top ICD-10 problems over time
│   ├── analysis_icd10_top_problems.py           # Analysis of top ICD-10 problems overall
│   ├── analysis_populacja_na_poradnie_geo.py    # Analysis of population per clinic geographically
│   ├── analysis_poradnie_pow_geo.py            # Geographical analysis of clinics at county level
│   ├── analysis_poradnie_woj_geo.py            # Geographical analysis of clinics at regional level
│   ├── analysis_poradnie_woj_time.py           # Time-series analysis of clinics at regional level
│   ├── analysis_porady_na_poradnie_geo.py      # Analysis of consultations per clinic geographically
│   ├── helpers/                                 # Utility scripts and configuration
│       ├── config.py                            # Project configuration variables
│       ├── utils.py                             # General utility functions
│       ├── matplotlib_utils.py                  # Utilities for Matplotlib plots
│-- doc/                        # Documentation files
│   ├── raport.pdf               # Final project report
│-- .gitignore                  # Git ignore file for untracked files
│-- environment.yml             # Conda environment configuration
│-- LICENSE                     # License for the project
│-- README.md                   # Project documentation
```

## Setup
Create a Conda environment:
```bash
conda env create -f environment.yml
conda activate mz_raport
```
## Data and Results

### Ophthalmology Clinic Data:
The data used in the analysis is available at the following link:  
[Ophthalmology Clinic Data](https://1drv.ms/f/c/aa7aab61d1edb18a/EqKSbQBWaeNIjQ6Z9PFSQRwBF3dwfWb0VZDY_8vC2IfElg?e=RAbKKn)

### Results:
The analysis results can be accessed at the following link:  
[Analysis Results](https://1drv.ms/f/c/aa7aab61d1edb18a/EmJKywdxpjJJoseLdyaErwsBVGoXW3L5ka0mG_ZxqVP-LA?e=HyKd8D)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
