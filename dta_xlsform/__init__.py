"""
dta_xlsform - Convert Stata .dta and SPSS .sav files to XLSForm format

A Python library to read Stata .dta and SPSS .sav files and convert them to XLSForm format
for use with data collection tools like ODK and KoboToolbox.
"""

from .converter import (
    DataToXLSForm,
    StataToXLSForm,  # Backward compatibility alias
    data_to_xlsform,
    stata_to_xlsform,
    spss_to_xlsform
)

__version__ = "0.2.0"
__all__ = [
    "DataToXLSForm",
    "StataToXLSForm",
    "data_to_xlsform",
    "stata_to_xlsform",
    "spss_to_xlsform"
]
