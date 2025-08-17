"""
Application constants and configuration values.
Single source of truth for UI strings, sizes, and other configuration values.
"""

class UIStrings:
    """UI text constants."""
    # Language and method selection
    SELECT_LANGUAGE = "Select language"
    SELECT_METHOD = "Select method"
    
    # Labels
    LANGUAGE_LABEL = "Language:"
    METHOD_LABEL = "Method:"
    
    # Buttons
    SAVE_LINES_TMX = "Save lines to TMX"
    CLEAR = "Clear"
    TRANSLITERATE = "Transliterate"
    
    # Checkboxes
    MATCH_ALL_CAPS = "Match ALL CAPS"
    
    # Window and section titles
    WINDOW_TITLE = "xlit-tool"
    SELECT_LANGUAGE_METHOD_SECTION = " Select language and transliteration method: "
    ENTER_TEXT_SECTION = " Enter your text: "
    ENTER_PASTE_TEXT = "Enter or paste text below:"
    
    # Menu items
    ABOUT_MENU = "&About"
    ABOUT_ITEM = "About"
    ABOUT_INFO = "Information about this program"
    SETTINGS_MENU = "&Settings"
    FONT_SIZE_SUBMENU = "Font size"
    
    # About dialog content
    APP_NAME = "xlit-tool"
    APP_VERSION = "1.0"
    APP_DESCRIPTION = "A cross-platform desktop transliteration tool for converting text between different writing systems, primarily from Cyrillic scripts to English using various romanization standards."
    APP_LICENSE = "This program is licensed under the MIT License."
    APP_DEVELOPER = "Steve Robertson"
    
    # Dialog titles and messages
    ERROR_TITLE = "Error"
    WARNING_TITLE = "Warning"
    INFO_TITLE = "Information"
    
    # TMX Export messages
    TMX_NO_INPUT_TITLE = "No Input Text"
    TMX_NO_INPUT_MSG = "Please enter some text to transliterate before exporting to TMX."
    TMX_NO_OUTPUT_TITLE = "No Output Text"
    TMX_NO_OUTPUT_MSG = "Please transliterate the text first before exporting to TMX."
    TMX_SAVE_DIALOG_TITLE = "Save TMX file"
    TMX_FILE_FILTER = "TMX files (*.tmx)|*.tmx|All files (*.*)|*.*"
    TMX_EXPORT_SUCCESS_TITLE = "Export Successful"
    TMX_EXPORT_SUCCESS_MSG = "TMX file exported successfully!\n\nSaved to: {path}"
    TMX_EXPORT_FAILED_TITLE = "Export Failed"
    TMX_EXPORT_FAILED_MSG = "Failed to export TMX file:\n{error}"
    TMX_EXPORT_ERROR_TITLE = "Export Error"
    TMX_EXPORT_ERROR_MSG = "An unexpected error occurred while exporting to TMX. Please try again."
    
    # Error messages
    INTERFACE_UPDATE_ERROR = "An error occurred while updating the interface."
    TEXT_CLEAR_ERROR = "An error occurred while clearing the text fields."
    TRANSLITERATION_ERROR_TITLE = "Transliteration Error"
    TRANSLITERATION_UNEXPECTED_ERROR = "An unexpected error occurred. Please try again or contact support if the problem persists."
    TRANSLITERATION_WARNINGS_TITLE = "Transliteration Warnings"
    TRANSLITERATION_WARNINGS_MSG = "Transliteration completed with the following warnings:\n\n{warnings}"


class AppConfig:
    """Application configuration constants."""
    # Window dimensions
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 630
    WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Font sizes
    DEFAULT_FONT_SIZE = 12
    AVAILABLE_FONT_SIZES = [10, 12, 14, 16, 18]
    
    # File paths and extensions
    TMX_EXTENSION = ".tmx"
    ICON_FILENAME = "transliterator.png"
    
    # Default directories
    DEFAULT_TMX_DIR = "~/Documents"
    
    # Configuration keys
    CONFIG_APP_NAME = "xlit-tool"
    CONFIG_FONT_SIZE_KEY = "FontSize"
    CONFIG_LAST_EXPORT_DIR_KEY = "LastExportDir"
    
    # Layout constants
    BORDER_SIZE = 10
    SMALL_BORDER = 5
    
    # Text control sizes
    TEXT_CTRL_WIDTH = 425
    TEXT_CTRL_HEIGHT = 300
    
    # Combo box sizes
    LANGUAGE_COMBO_WIDTH = 200
    METHOD_COMBO_WIDTH = 300


class FileConstants:
    """File-related constants."""
    # File extensions
    TMX_EXTENSION = ".tmx"
    
    # File patterns for dialogs
    TMX_WILDCARD = "TMX files (*.tmx)|*.tmx|All files (*.*)|*.*"
    
    # Default filenames
    DEFAULT_TMX_FILENAME_PATTERN = "transliteration_{timestamp}.tmx"


class LogMessages:
    """Logging message templates."""
    # Application lifecycle
    APP_STARTING = "Starting xlit-tool application"
    APP_STARTED = "Application started successfully"
    
    # Registry messages
    REGISTRY_VALIDATED = "Method registry validated successfully: {method_count} methods, {language_count} languages"
    METHOD_DISCOVERED = "Discovered method: {method_name}"
    METHOD_IMPORT_WARNING = "Could not import method module {module_name}: {error}"
    REGISTRY_IMPORT_ERROR = "Could not import transliteration_methods package: {error}"
    REGISTRY_VALIDATION_ERROR = "Method registry validation failed:\n{errors}"
    
    # Transliteration messages
    TRANSLITERATION_SUCCESS = "Successfully transliterated {char_count} characters using {method_name}"
    TRANSLITERATION_WARNINGS = "Transliteration completed with warnings: {warnings}"
    
    # TMX export messages
    TMX_EXPORT_SUCCESS = "TMX export successful: {file_path}"
    
    # Error handling
    COMBOBOX_CHANGE_ERROR = "Error handling combobox change: {error}"
    LANGUAGE_CHANGE_ERROR = "Error handling language change: {error}"
    TEXT_CLEAR_ERROR = "Error clearing text fields: {error}"
    TMX_EXPORT_UNEXPECTED_ERROR = "Unexpected error in TMX export handler: {error}"
    TRANSLITERATION_UNEXPECTED_ERROR = "Unexpected error in transliteration handler: {error}"


class ValidationMessages:
    """Input validation message templates."""
    # Text validation
    TEXT_TOO_SHORT = "Text must be at least {min_length} character(s) long"
    TEXT_TOO_LONG = "Text must be no more than {max_length} characters long"
    TEXT_LINE_TOO_LONG = "Lines must be no more than {max_length} characters long"
    TEXT_TOO_MANY_LINES = "Text must have no more than {max_lines} lines"
    TEXT_EMPTY = "Text cannot be empty"
    TEXT_CONTAINS_DANGEROUS_CONTENT = "Text contains potentially dangerous content that has been removed"
    
    # Method validation
    INVALID_METHOD = "Invalid transliteration method: {method_name}"
    METHOD_NOT_FOUND = "Transliteration method '{method_name}' not found"
    METHOD_CONFIG_ERROR = "The selected transliteration method is not properly configured"
    
    # Registry validation
    MISSING_DISPLAY_NAME = "Missing display name for method: {method_name}"
    METHOD_NOT_IN_REGISTRY = "Method '{method_name}' in language '{language}' not found in methods"
    NO_CASE_METHOD_NOT_FOUND = "No-case-match method '{method_name}' not found in methods"