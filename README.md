# mz_raport

This project is part of a recruitment task for the Ministry of Health, aiming to create a synthetic report on health issues reported by patients within ophthalmology outpatient clinics. The report will analyze the state of ophthalmology clinics, including the number of facilities and the volume of provided healthcare services related to various health problems of patients. A crucial aspect of the report is to capture the temporal variability of observed phenomena.

The report is intended for management purposes, with the Minister of Health as the primary audience.

## Project Structure

```
├── data/               # Data files
├── logs/              # Log files
├── notebooks/         # Jupyter notebooks
├── plots/             # Generated plots
├── results/           # Output results
├── src/               # Source code
│   ├── __init__.py
│   ├── main.py
│   └── helpers/        # Configuration and utility functions
├── .env              # Environment variables
├── .gitignore        # Git ignore file
├── environment.yml   # Conda environment file
├── pyproject.toml    # Project configuration and dependencies
├── LICENSE           # License for the project
└── README.md         # Project documentation
```

## Setup

### Option 1: Using Conda (Recommended)
1. Create a Conda environment:
```bash
conda env create -f environment.yml
conda activate mz_raport
```

2. Install the project in development mode:
```bash
pip install -e ".[dev,jupyter]"
```

### Option 2: Using venv
1. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

2. Install the project with development dependencies:
```bash
pip install -e ".[dev,jupyter]"
```

## Available Extra Dependencies

- Development tools (testing, linting): `pip install -e ".[dev]"`
- Jupyter notebook support: `pip install -e ".[jupyter]"`
- All optional dependencies: `pip install -e ".[dev,jupyter]"`

## Development Tools

This template includes several development tools configured in `pyproject.toml`:

- **black**: Code formatting
- **flake8**: Code linting
- **isort**: Import sorting
- **pytest**: Testing framework

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
