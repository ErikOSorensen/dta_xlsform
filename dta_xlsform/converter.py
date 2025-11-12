"""
Statistical Data to XLSForm Converter

A Python library to read Stata .dta and SPSS .sav files and convert them to XLSForm format.
XLSForm is a standard for creating forms for data collection tools like ODK and KoboToolbox.
"""

import pandas as pd
import pyreadstat
from typing import Dict, List, Tuple, Optional
import os


class DataToXLSForm:
    """
    Main class for converting Stata .dta or SPSS .sav files to XLSForm format.

    Attributes:
        file_path (str): Path to the data file (.dta or .sav)
        file_type (str): Type of file ('stata' or 'spss')
        df (pd.DataFrame): The data from the file
        metadata (pyreadstat.metadata_container): Metadata from the file
        variable_labels (Dict[str, str]): Dictionary of variable labels
        value_labels (Dict[str, Dict[int, str]]): Dictionary of value labels
    """

    def __init__(self, file_path: str, file_type: Optional[str] = None):
        """
        Initialize the converter with a Stata or SPSS file.

        Args:
            file_path (str): Path to the data file (.dta or .sav)
            file_type (str, optional): File type ('stata' or 'spss').
                                      If None, will be inferred from extension.

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a valid Stata or SPSS file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        self.file_path = file_path
        self.df = None
        self.metadata = None
        self.variable_labels = {}
        self.value_labels = {}

        # Infer file type from extension if not provided
        if file_type is None:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.dta':
                self.file_type = 'stata'
            elif ext == '.sav':
                self.file_type = 'spss'
            else:
                raise ValueError(f"Cannot infer file type from extension '{ext}'. "
                               "Please specify file_type='stata' or file_type='spss'")
        else:
            self.file_type = file_type.lower()

        self._read_file()

    def _read_file(self):
        """Read the data file and extract metadata."""
        try:
            if self.file_type == 'stata':
                # Try reading with different encodings to handle Scandinavian and other special characters
                encodings = ['utf-8', 'windows-1252', 'iso-8859-1', 'latin1']

                for encoding in encodings:
                    try:
                        self.df, self.metadata = pyreadstat.read_dta(
                            self.file_path,
                            encoding=encoding
                        )
                        break  # If successful, exit the loop
                    except (UnicodeDecodeError, Exception) as enc_error:
                        if encoding == encodings[-1]:  # Last encoding attempt
                            raise enc_error
                        continue  # Try next encoding
            elif self.file_type == 'spss':
                self.df, self.metadata = pyreadstat.read_sav(self.file_path)
            else:
                raise ValueError(f"Unsupported file type: {self.file_type}")

            # Extract variable labels
            if self.metadata.column_names_to_labels:
                self.variable_labels = self.metadata.column_names_to_labels

            # Extract value labels
            # Check if variable_value_labels contains label names (old format) or label dicts (new format)
            if self.metadata.variable_value_labels:
                for var_name, label_value in self.metadata.variable_value_labels.items():
                    if isinstance(label_value, dict):
                        # New format: value labels are directly in variable_value_labels
                        self.value_labels[var_name] = label_value
                    elif isinstance(label_value, str) and label_value in self.metadata.value_labels:
                        # Old format: variable_value_labels contains label names
                        self.value_labels[var_name] = self.metadata.value_labels[label_value]

        except Exception as e:
            raise ValueError(f"Error reading {self.file_type.upper()} file: {str(e)}")

    def _infer_question_type(self, var_name: str, dtype: str) -> str:
        """
        Infer XLSForm question type based on variable characteristics.

        Args:
            var_name (str): Variable name
            dtype (str): Data type of the variable

        Returns:
            str: XLSForm question type (e.g., 'select_one', 'integer', 'text', 'decimal')
        """
        # If variable has value labels, it's a select_one question
        if var_name in self.value_labels:
            return f"select_one {var_name}_choices"

        # Infer type from dtype
        if pd.api.types.is_integer_dtype(self.df[var_name]):
            return "integer"
        elif pd.api.types.is_float_dtype(self.df[var_name]):
            return "decimal"
        elif pd.api.types.is_bool_dtype(self.df[var_name]):
            return "select_one yes_no"
        else:
            return "text"

    def generate_survey_sheet(self) -> pd.DataFrame:
        """
        Generate the 'survey' sheet for XLSForm.

        Returns:
            pd.DataFrame: DataFrame containing the survey sheet structure
        """
        survey_data = []

        for var_name in self.df.columns:
            # Get variable label (question text)
            label = self.variable_labels.get(var_name, var_name)

            # Infer question type
            question_type = self._infer_question_type(var_name, str(self.df[var_name].dtype))

            survey_data.append({
                'type': question_type,
                'name': var_name,
                'label': label
            })

        return pd.DataFrame(survey_data)

    def generate_choices_sheet(self) -> pd.DataFrame:
        """
        Generate the 'choices' sheet for XLSForm.

        Returns:
            pd.DataFrame: DataFrame containing the choices sheet structure
        """
        choices_data = []

        # Add standard yes/no choices
        choices_data.append({
            'list_name': 'yes_no',
            'name': '1',
            'label': 'Yes'
        })
        choices_data.append({
            'list_name': 'yes_no',
            'name': '0',
            'label': 'No'
        })

        # Add choices from value labels
        for var_name, value_label_dict in self.value_labels.items():
            list_name = f"{var_name}_choices"

            for value, label in value_label_dict.items():
                choices_data.append({
                    'list_name': list_name,
                    'name': str(value),
                    'label': label
                })

        return pd.DataFrame(choices_data)

    def generate_settings_sheet(self, form_id: Optional[str] = None,
                                form_title: Optional[str] = None) -> pd.DataFrame:
        """
        Generate the 'settings' sheet for XLSForm.

        Args:
            form_id (str, optional): Unique form identifier
            form_title (str, optional): Human-readable form title

        Returns:
            pd.DataFrame: DataFrame containing the settings sheet structure
        """
        if form_id is None:
            # Use filename without extension as form_id
            form_id = os.path.splitext(os.path.basename(self.file_path))[0]

        if form_title is None:
            form_title = form_id.replace('_', ' ').title()

        settings_data = [{
            'form_title': form_title,
            'form_id': form_id
        }]

        return pd.DataFrame(settings_data)

    def to_xlsform(self, output_path: str, form_id: Optional[str] = None,
                   form_title: Optional[str] = None):
        """
        Generate and save the complete XLSForm Excel file.

        Args:
            output_path (str): Path where the XLSForm Excel file should be saved
            form_id (str, optional): Unique form identifier
            form_title (str, optional): Human-readable form title
        """
        # Generate all sheets
        survey_df = self.generate_survey_sheet()
        choices_df = self.generate_choices_sheet()
        settings_df = self.generate_settings_sheet(form_id, form_title)

        # Write to Excel file with multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            survey_df.to_excel(writer, sheet_name='survey', index=False)
            choices_df.to_excel(writer, sheet_name='choices', index=False)
            settings_df.to_excel(writer, sheet_name='settings', index=False)

        print(f"XLSForm successfully created: {output_path}")

    def get_variable_info(self) -> pd.DataFrame:
        """
        Get a summary of all variables with their labels and types.

        Returns:
            pd.DataFrame: DataFrame containing variable information
        """
        info_data = []

        for var_name in self.df.columns:
            info_data.append({
                'variable': var_name,
                'label': self.variable_labels.get(var_name, ''),
                'type': str(self.df[var_name].dtype),
                'has_value_labels': var_name in self.value_labels,
                'num_unique_values': self.df[var_name].nunique()
            })

        return pd.DataFrame(info_data)


# Backward compatibility: Keep old class name as alias
StataToXLSForm = DataToXLSForm


def data_to_xlsform(file_path: str, output_path: str,
                    form_id: Optional[str] = None,
                    form_title: Optional[str] = None,
                    file_type: Optional[str] = None) -> DataToXLSForm:
    """
    Convenience function to convert a Stata or SPSS file to XLSForm in one step.

    Args:
        file_path (str): Path to the data file (.dta or .sav)
        output_path (str): Path where the XLSForm Excel file should be saved
        form_id (str, optional): Unique form identifier
        form_title (str, optional): Human-readable form title
        file_type (str, optional): File type ('stata' or 'spss').
                                   If None, inferred from extension.

    Returns:
        DataToXLSForm: The converter instance (can be used for further inspection)

    Example:
        >>> converter = data_to_xlsform('data.dta', 'form.xlsx')
        >>> converter = data_to_xlsform('data.sav', 'form.xlsx')
        >>> print(converter.get_variable_info())
    """
    converter = DataToXLSForm(file_path, file_type)
    converter.to_xlsform(output_path, form_id, form_title)
    return converter


def stata_to_xlsform(dta_path: str, output_path: str,
                     form_id: Optional[str] = None,
                     form_title: Optional[str] = None) -> DataToXLSForm:
    """
    Convenience function to convert a Stata file to XLSForm in one step.

    Args:
        dta_path (str): Path to the Stata .dta file
        output_path (str): Path where the XLSForm Excel file should be saved
        form_id (str, optional): Unique form identifier
        form_title (str, optional): Human-readable form title

    Returns:
        DataToXLSForm: The converter instance (can be used for further inspection)

    Example:
        >>> converter = stata_to_xlsform('data.dta', 'form.xlsx')
        >>> print(converter.get_variable_info())
    """
    return data_to_xlsform(dta_path, output_path, form_id, form_title, file_type='stata')


def spss_to_xlsform(sav_path: str, output_path: str,
                    form_id: Optional[str] = None,
                    form_title: Optional[str] = None) -> DataToXLSForm:
    """
    Convenience function to convert an SPSS file to XLSForm in one step.

    Args:
        sav_path (str): Path to the SPSS .sav file
        output_path (str): Path where the XLSForm Excel file should be saved
        form_id (str, optional): Unique form identifier
        form_title (str, optional): Human-readable form title

    Returns:
        DataToXLSForm: The converter instance (can be used for further inspection)

    Example:
        >>> converter = spss_to_xlsform('data.sav', 'form.xlsx')
        >>> print(converter.get_variable_info())
    """
    return data_to_xlsform(sav_path, output_path, form_id, form_title, file_type='spss')
