# dta_xlsform

A Python library to read Stata .dta files and convert them to XLSForm format. This tool extracts variable names, labels, and value labels from Stata files and generates XLSForm specifications compatible with data collection tools like ODK (Open Data Kit) and KoboToolbox.

## Features

- Read Stata .dta files (all versions supported by pyreadstat)
- Extract variable names, labels, and value labels
- Generate XLSForm-compliant Excel files with survey, choices, and settings sheets
- Automatic type inference (text, integer, decimal, select_one)
- Support for categorical variables with value labels
- Inspect variable metadata before conversion

## Installation

### From GitHub

```bash
pip install git+https://github.com/ErikOSorensen/dta_xlsform.git
```

### From source

```bash
git clone https://github.com/ErikOSorensen/dta_xlsform.git
cd dta_xlsform
pip install -e .
```

## Dependencies

- pandas >= 1.3.0
- pyreadstat >= 1.1.0
- openpyxl >= 3.0.0

## Quick Start

### Simple Conversion

```python
from dta_xlsform import stata_to_xlsform

# Convert Stata file to XLSForm in one line
converter = stata_to_xlsform('data.dta', 'output_form.xlsx')
```

### With Custom Settings

```python
from dta_xlsform import stata_to_xlsform

# Convert with custom form ID and title
converter = stata_to_xlsform(
    dta_path='data.dta',
    output_path='survey_form.xlsx',
    form_id='health_survey_2024',
    form_title='Community Health Survey 2024'
)
```

## Detailed Usage

### Inspect Variables Before Conversion

```python
from dta_xlsform import StataToXLSForm

# Create converter instance
converter = StataToXLSForm('data.dta')

# Get variable information
var_info = converter.get_variable_info()
print(var_info)

# Access variable labels
print(converter.variable_labels)

# Access value labels
print(converter.value_labels)

# Generate XLSForm
converter.to_xlsform('output_form.xlsx')
```

### Preview Generated Sheets

```python
from dta_xlsform import StataToXLSForm

converter = StataToXLSForm('data.dta')

# Preview survey sheet
survey_df = converter.generate_survey_sheet()
print(survey_df)

# Preview choices sheet
choices_df = converter.generate_choices_sheet()
print(choices_df)

# Preview settings sheet
settings_df = converter.generate_settings_sheet()
print(settings_df)
```

## XLSForm Output Structure

The generated Excel file contains three sheets:

### 1. survey Sheet

Contains the form questions with columns:
- `type`: Question type (text, integer, decimal, select_one)
- `name`: Variable name from Stata file
- `label`: Variable label from Stata file

### 2. choices Sheet

Contains the answer choices for categorical variables with columns:
- `list_name`: Name of the choice list
- `name`: Value code
- `label`: Value label from Stata

### 3. settings Sheet

Contains form metadata with columns:
- `form_title`: Human-readable form title
- `form_id`: Unique form identifier

## Question Type Inference

The library automatically infers XLSForm question types:

| Stata Variable Type | XLSForm Type |
|---------------------|--------------|
| Variable with value labels | `select_one [varname]_choices` |
| Integer (without value labels) | `integer` |
| Float/Double | `decimal` |
| Boolean | `select_one yes_no` |
| String | `text` |

## API Reference

### `stata_to_xlsform(dta_path, output_path, form_id=None, form_title=None)`

Convenience function to convert a Stata file to XLSForm in one step.

**Parameters:**
- `dta_path` (str): Path to the Stata .dta file
- `output_path` (str): Path where the XLSForm Excel file should be saved
- `form_id` (str, optional): Unique form identifier
- `form_title` (str, optional): Human-readable form title

**Returns:**
- `StataToXLSForm`: The converter instance

### `StataToXLSForm` Class

Main class for converting Stata files to XLSForm.

#### Methods:

- `__init__(dta_path)`: Initialize with a Stata file path
- `generate_survey_sheet()`: Generate the survey sheet DataFrame
- `generate_choices_sheet()`: Generate the choices sheet DataFrame
- `generate_settings_sheet(form_id=None, form_title=None)`: Generate the settings sheet DataFrame
- `to_xlsform(output_path, form_id=None, form_title=None)`: Generate and save complete XLSForm
- `get_variable_info()`: Get summary of all variables with metadata

#### Attributes:

- `df`: Pandas DataFrame containing the Stata data
- `metadata`: pyreadstat metadata container
- `variable_labels`: Dict mapping variable names to labels
- `value_labels`: Dict mapping variable names to value label dictionaries

## Example Workflow

```python
from dta_xlsform import StataToXLSForm

# 1. Load Stata file
converter = StataToXLSForm('household_survey.dta')

# 2. Inspect variables
print("Variables in dataset:")
print(converter.get_variable_info())

# 3. Check value labels for categorical variables
print("\nCategorical variables:")
for var, labels in converter.value_labels.items():
    print(f"{var}: {labels}")

# 4. Generate XLSForm
converter.to_xlsform(
    output_path='household_survey_form.xlsx',
    form_id='household_survey_v1',
    form_title='Household Survey - Version 1'
)

print("XLSForm created successfully!")
```

## Limitations and Notes

- The library creates basic XLSForm structures. You may need to manually add:
  - Skip logic and constraints
  - Question groups and repeats
  - Calculations and relevance conditions
  - Advanced question types (geopoint, image, etc.)

- All variables from the Stata file are included in the form. You may want to manually remove ID variables or other non-question fields.

- The library assumes categorical variables have value labels in Stata. Unlabeled categorical variables will be treated as integer/text fields.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Built with [pyreadstat](https://github.com/Roche/pyreadstat) for reading Stata files
- Compatible with [XLSForm](https://xlsform.org/) standard
- Designed for use with [ODK](https://getodk.org/) and [KoboToolbox](https://www.kobotoolbox.org/)
