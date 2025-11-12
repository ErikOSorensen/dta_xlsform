"""
Example usage of the dta_xlsform library
"""

from dta_xlsform import stata_to_xlsform, StataToXLSForm


def example_1_simple_conversion():
    """Simple one-line conversion"""
    print("Example 1: Simple conversion")
    print("-" * 50)

    # Convert Stata file to XLSForm in one line
    converter = stata_to_xlsform(
        dta_path='your_data.dta',
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


def example_3_detailed_usage():
    """Detailed usage with inspection of variables"""
    print("Example 3: Detailed usage with variable inspection")
    print("-" * 50)

    # Create converter instance
    converter = StataToXLSForm('your_data.dta')

    # Inspect variable information
    print("Variable Information:")
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


def example_4_inspect_metadata():
    """Inspect metadata without generating XLSForm"""
    print("Example 4: Inspect metadata only")
    print("-" * 50)

    # Create converter instance
    converter = StataToXLSForm('your_data.dta')

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
    # Note: Replace 'your_data.dta' with the actual path to your Stata file

    print("=" * 50)
    print("Stata to XLSForm Converter - Examples")
    print("=" * 50)
    print()

    # Uncomment the example you want to run:

    # example_1_simple_conversion()
    # example_2_with_custom_settings()
    # example_3_detailed_usage()
    # example_4_inspect_metadata()

    print("\nNote: Make sure to replace 'your_data.dta' with your actual file path!")
