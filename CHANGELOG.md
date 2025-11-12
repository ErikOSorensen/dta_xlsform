# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-11-12

### Added
- **SPSS Support**: Full support for SPSS .sav files
- New `DataToXLSForm` class as the main converter (replaces `StataToXLSForm`)
- New convenience functions:
  - `spss_to_xlsform()` - Convert SPSS files
  - `data_to_xlsform()` - Universal converter with auto-detection
- Automatic file type detection from file extension (.dta or .sav)
- Multiple encoding support for Stata files (utf-8, windows-1252, iso-8859-1, latin1)

### Changed
- Main class renamed from `StataToXLSForm` to `DataToXLSForm`
- `file_path` attribute replaces `dta_path` to be more generic
- Updated all documentation and examples to show both Stata and SPSS usage

### Maintained
- Full backward compatibility with `StataToXLSForm` (kept as alias)
- All existing `stata_to_xlsform()` functionality preserved

## [0.1.0] - 2025-11-12

### Added
- Initial release
- Support for Stata .dta files
- Extract variable names, labels, and value labels
- Generate XLSForm-compliant Excel files (survey, choices, settings sheets)
- Automatic question type inference
- Variable metadata inspection
