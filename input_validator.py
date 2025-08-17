"""
Input validation and sanitization module for the xlit-tool application.
Provides comprehensive validation and sanitization for user inputs.
"""

import re
import unicodedata
import logging
from method_registry import get_method_registry

logger = logging.getLogger(__name__)

class InputValidator:
    """Handle input validation and sanitization."""
    
    def __init__(self):
        # Text length limits
        self.MIN_TEXT_LENGTH = 1
        self.MAX_TEXT_LENGTH = 250000
        self.MAX_LINE_LENGTH = 10000  # Maximum characters per line
        self.MAX_LINES = 5000         # Maximum number of lines
        
        # Dangerous patterns to detect and block
        self.DANGEROUS_PATTERNS = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',                # JavaScript URLs
            r'data:.*base64',             # Base64 data URLs
            r'vbscript:',                 # VBScript URLs
            r'on\w+\s*=',                # Event handlers (onclick, onload, etc.)
        ]
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE | re.DOTALL) 
                                for pattern in self.DANGEROUS_PATTERNS]
        
        # Get valid methods from registry
        self.registry = get_method_registry()
        self.VALID_METHODS = self.registry.get_valid_method_names()
    
    def validate_text_length(self, text):
        """
        Validate text length constraints.
        
        Args:
            text (str): Text to validate
            
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []
        
        if not text or len(text.strip()) < self.MIN_TEXT_LENGTH:
            errors.append("Text must contain at least 1 character")
            return False, errors
        
        if len(text) > self.MAX_TEXT_LENGTH:
            errors.append(f"Text exceeds maximum length of {self.MAX_TEXT_LENGTH:,} characters")
        
        # Check line count
        lines = text.split('\n')
        if len(lines) > self.MAX_LINES:
            errors.append(f"Text exceeds maximum of {self.MAX_LINES:,} lines")
        
        # Check individual line lengths
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > self.MAX_LINE_LENGTH]
        if long_lines:
            if len(long_lines) <= 3:
                line_list = ", ".join(map(str, long_lines))
                errors.append(f"Lines {line_list} exceed maximum length of {self.MAX_LINE_LENGTH:,} characters")
            else:
                errors.append(f"{len(long_lines)} lines exceed maximum length of {self.MAX_LINE_LENGTH:,} characters")
        
        return len(errors) == 0, errors
    
    def validate_method_name(self, method_name):
        """
        Validate transliteration method name.
        
        Args:
            method_name (str): Method name to validate
            
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []
        
        if not method_name or not method_name.strip():
            errors.append("Please select a transliteration method")
            return False, errors
        
        if method_name == "Select method":
            errors.append("Please select a valid transliteration method")
            return False, errors
        
        if method_name not in self.VALID_METHODS:
            errors.append(f"Invalid transliteration method: {method_name}")
            return False, errors
        
        return True, errors
    
    def detect_dangerous_content(self, text):
        """
        Detect potentially dangerous content in text.
        
        Args:
            text (str): Text to scan
            
        Returns:
            tuple: (has_dangerous_content: bool, detected_patterns: list)
        """
        detected = []
        
        for i, pattern in enumerate(self.compiled_patterns):
            if pattern.search(text):
                detected.append(self.DANGEROUS_PATTERNS[i])
        
        return len(detected) > 0, detected
    
    def sanitize_text(self, text, preserve_formatting=True):
        """
        Sanitize input text while preserving transliteration-relevant content.
        
        Args:
            text (str): Text to sanitize
            preserve_formatting (bool): Whether to preserve line breaks and basic formatting
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Normalize Unicode characters
        text = unicodedata.normalize('NFC', text)
        
        # Remove dangerous patterns
        for pattern in self.compiled_patterns:
            text = pattern.sub('', text)
        
        # Remove control characters except allowed ones
        if preserve_formatting:
            # Keep line breaks, carriage returns, and tabs
            allowed_control = {'\n', '\r', '\t'}
            text = ''.join(char for char in text 
                          if not unicodedata.category(char).startswith('C') 
                          or char in allowed_control)
        else:
            # Remove all control characters
            text = ''.join(char for char in text 
                          if not unicodedata.category(char).startswith('C'))
        
        # Remove excessive whitespace while preserving intentional formatting
        if preserve_formatting:
            # Remove trailing/leading whitespace from each line
            lines = text.split('\n')
            lines = [line.rstrip() for line in lines]
            text = '\n'.join(lines)
            
            # Remove excessive consecutive empty lines (max 2)
            text = re.sub(r'\n{4,}', '\n\n\n', text)
        else:
            # Normalize all whitespace to single spaces
            text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def validate_and_sanitize_input(self, text, method_name, sanitize=True):
        """
        Comprehensive validation and sanitization of user input.
        
        Args:
            text (str): Input text to validate and sanitize
            method_name (str): Transliteration method name
            sanitize (bool): Whether to sanitize the text
            
        Returns:
            dict: {
                'is_valid': bool,
                'sanitized_text': str,
                'errors': list,
                'warnings': list
            }
        """
        result = {
            'is_valid': True,
            'sanitized_text': text,
            'errors': [],
            'warnings': []
        }
        
        # Validate method name
        method_valid, method_errors = self.validate_method_name(method_name)
        if not method_valid:
            result['errors'].extend(method_errors)
            result['is_valid'] = False
        
        # Early return if text is None
        if text is None:
            result['errors'].append("Input text cannot be None")
            result['is_valid'] = False
            return result
        
        # Sanitize text if requested
        if sanitize:
            original_length = len(text)
            result['sanitized_text'] = self.sanitize_text(text)
            
            # Warn if sanitization changed the text significantly
            if len(result['sanitized_text']) < original_length * 0.95:
                result['warnings'].append("Text was modified during sanitization (potentially unsafe content removed)")
        
        # Validate text length
        length_valid, length_errors = self.validate_text_length(result['sanitized_text'])
        if not length_valid:
            result['errors'].extend(length_errors)
            result['is_valid'] = False
        
        # Check for dangerous content
        has_dangerous, dangerous_patterns = self.detect_dangerous_content(result['sanitized_text'])
        if has_dangerous:
            result['warnings'].append(f"Potentially unsafe content detected: {', '.join(dangerous_patterns)}")
            logger.warning(f"Dangerous content detected in input: {dangerous_patterns}")
        
        return result
