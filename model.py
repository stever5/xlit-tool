# model.py

import logging
from typing import Tuple, List, Dict, Any
from transliteration_methods import utils
from input_validator import InputValidator
from method_registry import get_method_registry

logger = logging.getLogger(__name__)

class XlitToolError(Exception):
    """Custom exception for transliteration errors."""
    pass

class XlitToolModel:
    def __init__(self):
        self.validator = InputValidator()
        self.registry = get_method_registry()
        
        # For backward compatibility, expose methods as property
        self.methods = self.registry.get_all_methods()


    def get_languages(self) -> List[str]:
        """Return a list of available languages."""
        return self.registry.get_languages()

    def get_transliteration_methods(self) -> List[str]:
        """Return all transliteration methods (legacy method for backward compatibility)."""
        return ["Select method"] + list(self.methods.keys())

    def get_methods_by_language(self, language: str) -> List[str]:
        """Return transliteration methods for a specific language."""
        return self.registry.get_methods_by_language(language)

    def get_method_display_name(self, method_name: str) -> str:
        """Return the display name for a method."""
        return self.registry.get_display_name(method_name)

    def get_method_from_display_name(self, display_name: str, language: str) -> str:
        """Return the full method name from a display name within a language context."""
        return self.registry.get_method_from_display_name(display_name, language)


    def validate_and_sanitize_input(self, method_name: str, text: str, sanitize: bool = True) -> Dict[str, Any]:
        """
        Validate and sanitize input parameters for transliteration.
        
        Args:
            method_name: Name of the transliteration method
            text: Text to transliterate
            sanitize: Whether to sanitize the input text
            
        Returns:
            Validation result with sanitized text, errors, and warnings
        """
        return self.validator.validate_and_sanitize_input(text, method_name, sanitize)

    def transliterate(self, method_name: str, text: str, match_case: bool, sanitize_input: bool = True) -> Tuple[bool, str, str, List[str]]:
        """
        Transliterate text using the specified method.
        
        Args:
            method_name: Name of the transliteration method
            text: Text to transliterate
            match_case: Whether to preserve case matching
            sanitize_input: Whether to sanitize input text
            
        Returns:
            Tuple of (success, result, error_message, warnings)
        """
        try:
            # Validate and sanitize inputs
            validation_result = self.validate_and_sanitize_input(method_name, text, sanitize_input)
            
            if not validation_result['is_valid']:
                error_msg = "\n".join(validation_result['errors'])
                logger.warning(f"Input validation failed: {error_msg}")
                return False, "", error_msg, validation_result['warnings']
            
            # Use sanitized text for transliteration
            sanitized_text = validation_result['sanitized_text']
            warnings = validation_result['warnings']
            
            method = self.methods.get(method_name)
            if not method:
                error_msg = f"Transliteration method '{method_name}' not found"
                logger.error(error_msg)
                return False, "", error_msg, warnings

            # Perform transliteration
            if match_case:
                result = utils.transliterate_case_match(sanitized_text, method)
            else:
                result = method.transliterate(sanitized_text)
            
            logger.info(f"Successfully transliterated {len(sanitized_text)} characters using {method_name}")
            if warnings:
                logger.info(f"Transliteration completed with warnings: {'; '.join(warnings)}")
            
            return True, result, "", warnings
            
        except AttributeError as e:
            error_msg = f"Transliteration method error: {str(e)}"
            logger.error(error_msg)
            return False, "", "The selected transliteration method is not properly configured", []
        except Exception as e:
            error_msg = f"Unexpected error during transliteration: {str(e)}"
            logger.error(error_msg)
            return False, "", "An unexpected error occurred during transliteration", []


    def should_enable_match_case(self, method_name: str) -> bool:
        """Check if a method supports case matching."""
        return self.registry.should_enable_case_match(method_name)

