# xlit-tool

A cross-platform desktop transliteration tool for converting text between different writing systems, primarily from Cyrillic scripts to English using various romanization standards.

## Overview

This application provides accurate transliteration for 25 different transliteration methods covering Slavic, Turkic, and other languages using Cyrillic scripts. Built with Python and wxPython, it offers a user-friendly desktop interface with comprehensive error handling and validation.

## Features

- **25 Transliteration Methods** covering major Cyrillic-based languages
- **Multiple Romanization Standards** (IC, BGN, ALA-LC, ISO-9, Scientific, GOST)
- **Case Matching** option to preserve original text casing
- **Input Validation** with comprehensive error handling
- **TMX Export** for translation memory integration
- **Batch Processing** with file import/export capabilities
- **Comprehensive Test Suite** with 115 test cases

## Supported Languages & Methods

### Slavic Languages
- **Russian**: 8 romanization systems (IC, BGN, ALA-LC, ISO-9, Scientific, GOST, Chinese Pinyin, Japanese Hepburn)
- **Ukrainian**: 3 systems (IC, National Standard, Chinese Academic)
- **Belarusian**: IC system with ў character
- **Bulgarian**: IC system with regex pattern optimization
- **Serbian**: IC system with special characters (ђ, љ, њ, ћ, џ)
- **Macedonian**: IC system with characters (ѓ, ѕ, љ, њ, ќ, џ)

### Turkic Languages
- **Kazakh**: IC system with characters (ғ, қ, ң, ө, ұ, ү, һ, і)
- **Kyrgyz**: IC system with characters (ң, ө, ү)
- **Uzbek**: IC system with ў character
- **Tatar**: IC system with ң character
- **Turkmen**: IC system with ң character
- **Azeri**: IC system

### Other Languages
- **Tajik**: IC system with characters (ғ, қ, ҳ, ҷ)
- **Georgian**: IC system (special handling)
- **Uyghur**: IC system

### Special Systems
- **Russian Chinese Cyrillic → English (Pinyin)**: Chinese transliteration of Russian
- **Russian Japanese Cyrillic → English (Hepburn)**: Japanese transliteration of Russian
- **Ukrainian Chinese Academic → English**: Academic Chinese transliteration of Ukrainian

## Installation

### Requirements
- Python 3.7 or higher
- wxPython 4.0 or higher

### Setup
1. **Clone or download** the application files
2. **Install dependencies**:
   ```bash
   pip install wxpython
   ```
3. **Navigate to the application directory**:
   ```bash
   cd /path/to/transliterator/app/MVC_version
   ```

## Running the Application

### Desktop GUI
```bash
python __main__.py
```

This launches the wxPython desktop interface with:
- **Input text area** for source text
- **Output text area** for transliterated results
- **Method selection** dropdown
- **Case matching** checkbox option
- **Clear, Copy, Export** buttons
- **File import/export** functionality

### GUI Features
- **Real-time transliteration** as you type
- **Error dialogs** for invalid input or method issues
- **TMX export** for translation memory systems
- **Input validation** with user-friendly error messages
- **Character limit**: 250,000 characters maximum

## Running Tests

The application includes a comprehensive test suite with command-line utilities for efficient testing.

### Basic Test Execution

#### Run All Tests
```bash
python comprehensive_test_suite.py
```
Executes all 115 test cases across 25 methods (~0.03 seconds)

#### Show Test Coverage Summary
```bash
python comprehensive_test_suite.py --summary
```
Quick overview of test coverage without running tests (~0.01 seconds)

### Targeted Testing

#### Test Specific Method
```bash
python comprehensive_test_suite.py --method "Russian (Cyrillic)-->English (IC)"
```
Run tests for a single transliteration method only

#### Run Only Failed Tests
```bash
python comprehensive_test_suite.py --failed-only
```
Execute only tests that are currently failing (faster debugging)

#### Combination Testing
```bash
python comprehensive_test_suite.py --method "Ukrainian (Cyrillic)-->English (IC)" --failed-only
```
Run only failing tests for a specific method (most focused option)

### Test Command Reference

| Command | Purpose | Execution Time | Use Case |
|---------|---------|---------------|-----------|
| `python comprehensive_test_suite.py` | Run all tests | ~0.03s | Full validation |
| `--summary` | Coverage overview | ~0.01s | Quick status |
| `--method "Method Name"` | Single method | ~0.01s | Focused testing |
| `--failed-only` | Failed tests only | ~0.03s | Issue identification |
| `--help` | Usage information | Instant | Command reference |

### Test Output

Tests generate detailed reports including:
- **Pass/fail status** for each test case
- **Expected vs actual** output for failures
- **Method-wise statistics** and success rates
- **Detailed failure reports** with descriptions
- **JSON result files** with timestamps for tracking

## Application Architecture

### MVC Design Pattern
- **Model** (`model.py`): Core transliteration logic and business rules
- **View** (`view.py`): wxPython GUI interface and user interactions
- **Controller** (`controller.py`): Coordination between model and view

### Key Components
- **Input Validator** (`input_validator.py`): Text validation and sanitization
- **TMX Exporter** (`tmx_exporter.py`): Translation memory export functionality
- **Config Manager** (`config_manager.py`): Application configuration handling
- **Transliteration Methods** (`transliteration_methods/`): Individual method implementations

### Error Handling
- **Comprehensive validation** of user input
- **Graceful error recovery** with user-friendly messages
- **Input sanitization** to prevent issues
- **Logging system** for debugging and monitoring

## File Structure

```
MVC_version/
├── README.md                          # This file
├── __main__.py                        # Application entry point
├── model.py                           # Core transliteration logic
├── view.py                            # wxPython GUI interface
├── controller.py                      # MVC controller
├── input_validator.py                 # Input validation and sanitization
├── tmx_exporter.py                    # TMX export functionality
├── config_manager.py                  # Configuration management
├── comprehensive_test_suite.py        # Test suite with CLI utilities
├── COMMAND_LINE_UTILITIES.md          # Test utilities documentation
├── PHASE1_REFACTORING_SUMMARY.md      # Phase 1 test refactoring details
├── PHASE2_REFACTORING_SUMMARY.md      # Phase 2 test refactoring details
├── README_TEST_SUITE.md               # Original test suite documentation
└── transliteration_methods/           # Individual method implementations
    ├── __init__.py
    ├── utils.py                       # Shared utilities
    ├── ru_cyr_en_ic.py               # Russian IC method
    ├── uk_cyr_en_ic.py               # Ukrainian IC method
    ├── kk_cyr_en_ic.py               # Kazakh IC method
    └── ...                           # Additional method files
```

## Usage Examples

### Basic Desktop Usage
1. **Launch the application**: `python __main__.py`
2. **Select transliteration method** from dropdown
3. **Enter text** in the input area
4. **View results** in the output area
5. **Export to TMX** if needed for translation memory

### Development Workflow
```bash
# Quick status check
python comprehensive_test_suite.py --summary

# Test specific method you're working on
python comprehensive_test_suite.py --method "Russian (Cyrillic)-->English (IC)"

# Check current issues
python comprehensive_test_suite.py --failed-only

# After fixes, run full test suite
python comprehensive_test_suite.py
```

### Debugging Character Mapping Issues
```bash
# Identify failing tests for specific method
python comprehensive_test_suite.py --method "Ukrainian (Cyrillic)-->English (IC)" --failed-only

# After character mapping fixes, retest
python comprehensive_test_suite.py --method "Ukrainian (Cyrillic)-->English (IC)"
```

## Test Coverage

The application includes comprehensive test coverage:

- **115 test cases** across all 25 methods
- **Character mapping tests** for special characters
- **Geographic name tests** (cities, countries, regions)
- **Sample text tests** with real-world phrases
- **Pattern matching tests** for regex-based methods
- **Case handling tests** for uppercase/lowercase scenarios

### Current Test Results
- **Total Success Rate**: 100%
- **Methods with 100% Pass Rate**: 25 out of 25
- **All Issues Resolved**: No known character mapping issues
- **Test Categories**: Alphabet, special characters, geographic names, sample texts

## Known Issues & Limitations

### Application Limitations
- **Input limit**: 250,000 characters maximum
- **Offline only**: No network connectivity required or supported
- **Single user**: Desktop application for individual use
- **Platform**: Requires Python environment with wxPython

## Contributing

### Running Tests Before Changes
```bash
# Get baseline test results
python comprehensive_test_suite.py > baseline_results.txt

# After making changes, compare results
python comprehensive_test_suite.py > new_results.txt
```

### Adding New Test Cases
Test cases use a standardized format in `comprehensive_test_suite.py`:

```python
{
    "name": "descriptive_test_name",
    "input": "text to transliterate",
    "expected": "expected output",
    "match_case": False,
    "description": "Human-readable description"
}
```

### Code Style Guidelines
- Follow existing MVC architecture patterns
- Use comprehensive error handling
- Include descriptive docstrings
- Add test cases for new functionality
- Maintain backward compatibility

## Performance

### Application Performance
- **Startup time**: ~1-2 seconds
- **Transliteration speed**: Real-time for typical input sizes
- **Memory usage**: Minimal for desktop application
- **File operations**: Fast import/export for reasonable file sizes

### Test Performance
- **Full test suite**: ~0.03 seconds (115 tests)
- **Single method**: ~0.01 seconds
- **Failed tests only**: ~0.03 seconds
- **Summary only**: ~0.01 seconds

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.7+

# Check wxPython installation
python -c "import wx; print(wx.version())"

# Reinstall wxPython if needed
pip install --upgrade wxpython
```

#### Test Failures
```bash
# Check for specific method issues
python comprehensive_test_suite.py --method "Method Name"

# See all current failures
python comprehensive_test_suite.py --failed-only

# Verify test suite integrity
python comprehensive_test_suite.py --summary
```

#### Import/Export Issues
- Ensure file paths are accessible
- Check file encoding (UTF-8 recommended)
- Verify file permissions for export location

### Getting Help

1. **Check test results** to identify specific issues
2. **Review error messages** in the GUI for user-friendly explanations
3. **Run diagnostic commands** to isolate problems
4. **Check file structure** to ensure all components are present

## License

MIT License - see [LICENSE](LICENSE) file for details.

This transliteration application is designed for educational and practical use in text processing and language conversion tasks.

---

**Last Updated**: 2025-01-17  
**Version**: 1.0 (Production Release)  
**Python Version**: 3.7+  
**GUI Framework**: wxPython 4.0+