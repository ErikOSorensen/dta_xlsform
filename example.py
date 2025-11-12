"""
Example usage of the dta_xlsform library

Demonstrates converting both Stata (.dta) and SPSS (.sav) files to XLSForm format.
"""

from dta_xlsform import (
    stata_to_xlsform,
    spss_to_xlsform,
    data_to_xlsform,
    DataToXLSForm
)


def example_1_simple_stata_conversion():
    """Simple one-line Stata conversion"""
    print("Example 1: Simple Stata conversion")
    print("-" * 50)

    # Convert Stata file to XLSForm in one line
    converter = stata_to_xlsform(
        dta_path='your_data.dta',
        output_path='output_form.xlsx'
    )

    print("Conversion complete!\n")


def example_1b_simple_spss_conversion():
    """Simple one-line SPSS conversion"""
    print("Example 1b: Simple SPSS conversion")
    print("-" * 50)

    # Convert SPSS file to XLSForm in one line
    converter = spss_to_xlsform(
        sav_path='your_data.sav',
        output_path='output_form.xlsx'
    )

    print("Conversion complete!\n")


def example_2_with_custom_settings():
    """Conversion with custom form settings"""
    print("Example 2: Conversion with custom settings")
    print("-" * 50)

    # Convert with custom form ID and title
    converter = stata_to_xlsform(
        dta_path='your_data.dta',
        output_path='output_form.xlsx',
        form_id='my_survey_2024',
        form_title='Community Health Survey 2024'
    )

    print("Conversion complete with custom settings!\n")


def example_3_auto_detect_file_type():
    """Auto-detect file type from extension"""
    print("Example 3: Auto-detect file type")
    print("-" * 50)

    # File type automatically detected from extension
    converter1 = data_to_xlsform('data.dta', 'stata_form.xlsx')
    print(f"Detected file type: {converter1.file_type}")

    converter2 = data_to_xlsform('data.sav', 'spss_form.xlsx')
    print(f"Detected file type: {converter2.file_type}")

    print("\nConversion complete!\n")


def example_4_detailed_stata_usage():
    """Detailed usage with inspection of Stata variables"""
    print("Example 4: Detailed Stata usage with variable inspection")
    print("-" * 50)

    # Create converter instance
    converter = DataToXLSForm('your_data.dta')

    # Check file type
    print(f"File type: {converter.file_type}")

    # Inspect variable information
    print("\nVariable Information:")
    var_info = converter.get_variable_info()
    print(var_info.to_string())
    print()

    # Preview survey sheet
    print("\nSurvey Sheet Preview:")
    survey_df = converter.generate_survey_sheet()
    print(survey_df.head(10).to_string())
    print()

    # Preview choices sheet
    print("\nChoices Sheet Preview:")
    choices_df = converter.generate_choices_sheet()
    print(choices_df.head(10).to_string())
    print()

    # Generate the XLSForm
    converter.to_xlsform(
        output_path='output_form.xlsx',
        form_title='My Custom Form'
    )

    print("\nConversion complete!\n")


def example_5_detailed_spss_usage():
    """Detailed usage with inspection of SPSS variables"""
    print("Example 5: Detailed SPSS usage with variable inspection")
    print("-" * 50)

    # Create converter instance for SPSS file
    converter = DataToXLSForm('your_data.sav')

    # Check file type
    print(f"File type: {converter.file_type}")

    # Inspect variable information
    print("\nVariable Information:")
    var_info = converter.get_variable_info()
    print(var_info.to_string())
    print()

    # Access value labels
    print("\nCategorical Variables:")
    for var_name, labels in converter.value_labels.items():
        print(f"  {var_name}: {len(labels)} categories")
    print()

    # Generate the XLSForm
    converter.to_xlsform(
        output_path='spss_output_form.xlsx',
        form_id='spss_survey_2024',
        form_title='SPSS Survey Form'
    )

    print("\nConversion complete!\n")


def example_6_inspect_metadata():
    """Inspect metadata without generating XLSForm"""
    print("Example 6: Inspect metadata only")
    print("-" * 50)

    # Works with both Stata and SPSS
    converter = DataToXLSForm('your_data.dta')  # or 'your_data.sav'

    # Access variable labels
    print("Variable Labels:")
    for var_name, label in converter.variable_labels.items():
        print(f"  {var_name}: {label}")
    print()

    # Access value labels
    print("\nValue Labels:")
    for var_name, value_dict in converter.value_labels.items():
        print(f"  {var_name}:")
        for value, label in value_dict.items():
            print(f"    {value}: {label}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("dta_xlsform - Stata & SPSS to XLSForm Converter - Examples")
    print("=" * 60)
    print()

    # Uncomment the example you want to run:

    # example_1_simple_stata_conversion()
    # example_1b_simple_spss_conversion()
    # example_2_with_custom_settings()
    # example_3_auto_detect_file_type()
    # example_4_detailed_stata_usage()
    # example_5_detailed_spss_usage()
    # example_6_inspect_metadata()

    print("\nNote: Replace 'your_data.dta' or 'your_data.sav' with your actual file paths!")
    print("The library supports both Stata (.dta) and SPSS (.sav) files.")
