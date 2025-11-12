"""
dta_xlsform - Convert Stata .dta files to XLSForm format

A Python library to read Stata .dta files and convert them to XLSForm format
for use with data collection tools like ODK and KoboToolbox.
"""

from .converter import StataToXLSForm, stata_to_xlsform

__version__ = "0.1.0"
__all__ = ["StataToXLSForm", "stata_to_xlsform"]
