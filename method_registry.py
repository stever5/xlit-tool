"""
Centralized registry for transliteration methods.
Single source of truth for all method discovery, organization, and metadata.
"""

import importlib
import logging
import re
from typing import Dict, List, Set, Optional, Any
from constants import UIStrings

logger = logging.getLogger(__name__)


class MethodRegistry:
    """
    Centralized registry that auto-discovers transliteration methods
    and provides metadata about them.
    """
    
    def __init__(self):
        self._methods: Dict[str, Any] = {}
        self._language_groups: Dict[str, List[str]] = {}
        self._display_names: Dict[str, str] = {}
        self._no_case_match: Set[str] = set()
        self._method_to_language: Dict[str, str] = {}
        
        self._discover_methods()
        self._organize_by_language()
        self._generate_display_names()
        self._identify_no_case_methods()
        self._generate_language_codes()
        
        # Validate the registry
        self._validate_registry()
    
    def _discover_methods(self) -> None:
        """Auto-discover all transliteration methods from the transliteration_methods package."""
        # Import the package to get __all__ list
        try:
            import transliteration_methods
            
            # Get all method modules from __all__
            method_modules = getattr(transliteration_methods, '__all__', [])
            
            # Add the missing Ukrainian methods that aren't in __all__
            additional_methods = [
                'uk_cyr_en_nat_standard',
                'ukr_cyr_chinese_academic_en'
            ]
            method_modules.extend(additional_methods)
            
            for module_name in method_modules:
                try:
                    module = importlib.import_module(f'transliteration_methods.{module_name}')
                    method_full_name = self._module_to_method_name(module_name)
                    self._methods[method_full_name] = module
                    logger.debug(f"Discovered method: {method_full_name}")
                except ImportError as e:
                    logger.warning(f"Could not import method module {module_name}: {e}")
                    
        except ImportError as e:
            logger.error(f"Could not import transliteration_methods package: {e}")
            raise
    
    def _module_to_method_name(self, module_name: str) -> str:
        """Convert module name to full method name."""
        # Mapping of module names to full method names
        module_mapping = {
            'az_cyr_en_ic': 'Azeri (Cyrillic)-->English (IC)',
            'be_cyr_en_ic': 'Belarussian (Cyrillic)-->English (IC)',
            'bg_cyr_en_ic': 'Bulgarian (Cyrillic)-->English (IC)',
            'ka_en_ic': 'Georgian (Cyrillic)-->English (IC)',
            'kk_cyr_en_ic': 'Kazakh (Cyrillic)-->English (IC)',
            'ky_cyr_en_ic': 'Kyrghyz (Cyrillic)-->English (IC)',
            'mk_cyr_en_ic': 'Macedonian (Cyrillic)-->English (IC)',
            'mn_cyr_en_mns': 'Mongolian (Cyrillic)-->English (MNS)',
            'ru_cyr_chinese_en': 'Russian (Chinese Cyrillic)-->English (Pinyin)',
            'ru_cyr_japanese_en': 'Russian (Japanese Cyrillic)-->English (Hepburn)',
            'ru_cyr_en_ala_lc': 'Russian (Cyrillic)-->English (ALA-LC)',
            'ru_cyr_en_bgn': 'Russian (Cyrillic)-->English (BGN)',
            'ru_cyr_en_gost_7_79_2000_system_b': 'Russian (Cyrillic)-->English (Gost 7.79-2000b)',
            'ru_cyr_en_ic': 'Russian (Cyrillic)-->English (IC)',
            'ru_cyr_en_iso_9': 'Russian (Cyrillic)-->English (ISO-9)',
            'ru_cyr_en_scientific': 'Russian (Cyrillic)-->English (Scientific)',
            'sr_cyr_en_ic': 'Serbian (Cyrillic)-->English (IC)',
            'tg_cyr_en_ic': 'Tajik (Cyrillic)-->English (IC)',
            'tt_cyr_en_ic': 'Tatar (Cyrillic)-->English (IC)',
            'tk_cyr_en_ic': 'Turkmen (Cyrillic)-->English (IC)',
            'uk_cyr_en_ic': 'Ukrainian (Cyrillic)-->English (IC)',
            'uk_cyr_en_nat_standard': 'Ukrainian (Cyrillic)-->English (National Standard)',
            'ukr_cyr_chinese_academic_en': 'Ukrainian (Chinese Academic)-->English',
            'ug_cyr_en_ic': 'Uyghur (Cyrillic)-->English (IC)',
            'uz_cyr_en_ic': 'Uzbek (Cyrillic)-->English (IC)',
        }
        
        return module_mapping.get(module_name, module_name)
    
    def _organize_by_language(self) -> None:
        """Organize methods by language."""
        language_patterns = {
            'Azerbaijani': r'Azeri.*',
            'Belarusian': r'Belarussian.*',
            'Bulgarian': r'Bulgarian.*',
            'Georgian': r'Georgian.*',
            'Kazakh': r'Kazakh.*',
            'Kyrgyz': r'Kyrghyz.*',
            'Macedonian': r'Macedonian.*',
            'Mongolian': r'Mongolian.*',
            'Russian': r'Russian.*',
            'Serbian': r'Serbian.*',
            'Tajik': r'Tajik.*',
            'Tatar': r'Tatar.*',
            'Turkmen': r'Turkmen.*',
            'Ukrainian': r'Ukrainian.*',
            'Uyghur': r'Uyghur.*',
            'Uzbek': r'Uzbek.*',
        }
        
        for language, pattern in language_patterns.items():
            matching_methods = [
                method for method in self._methods.keys()
                if re.match(pattern, method)
            ]
            if matching_methods:
                self._language_groups[language] = sorted(matching_methods)
    
    def _generate_display_names(self) -> None:
        """Generate display names for methods with special cases."""
        # Special cases that need custom display names
        special_cases = {
            'Russian (Chinese Cyrillic)-->English (Pinyin)': 'Chinese Pinyin (for Chinese Cyrillic text)',
            'Russian (Japanese Cyrillic)-->English (Hepburn)': 'Japanese Hepburn (for Japanese Cyrillic text)',
            'Ukrainian (Chinese Academic)-->English': 'Chinese Academic',
        }
        
        for method_name in self._methods.keys():
            if method_name in special_cases:
                self._display_names[method_name] = special_cases[method_name]
            else:
                # Extract method name from the full name
                # Pattern: "Language (Script)-->Target (Method)"
                match = re.search(r'\(([^)]+)\)$', method_name)
                if match:
                    self._display_names[method_name] = match.group(1)
                else:
                    # Fallback: use the method name after the last -->
                    parts = method_name.split('-->')
                    if len(parts) > 1:
                        self._display_names[method_name] = parts[-1].strip()
                    else:
                        self._display_names[method_name] = method_name
    
    def _identify_no_case_methods(self) -> None:
        """Identify methods that don't support case matching."""
        no_case_methods = {
            'Georgian (Cyrillic)-->English (IC)',
            'Russian (Chinese Cyrillic)-->English (Pinyin)',
            'Russian (Japanese Cyrillic)-->English (Hepburn)',
            'Russian (Cyrillic)-->English (ISO-9)',
            'Ukrainian (Chinese Academic)-->English',
        }
        
        self._no_case_match = {
            method for method in no_case_methods 
            if method in self._methods
        }
    
    def _generate_language_codes(self) -> None:
        """Generate language codes for TMX export."""
        language_code_mapping = {
            'Azeri': 'az', 'Belarussian': 'be', 'Bulgarian': 'bg', 'Georgian': 'ka',
            'Kazakh': 'kk', 'Kyrghyz': 'ky', 'Macedonian': 'mk', 'Mongolian': 'mn',
            'Russian': 'ru', 'Serbian': 'sr', 'Tajik': 'tg', 'Tatar': 'tt',
            'Turkmen': 'tk', 'Ukrainian': 'uk', 'Uyghur': 'ug', 'Uzbek': 'uz'
        }
        
        for method_name in self._methods.keys():
            for language_name, code in language_code_mapping.items():
                if method_name.startswith(language_name):
                    self._method_to_language[method_name] = code
                    break
    
    def _validate_registry(self) -> None:
        """Validate that the registry is properly configured."""
        errors = []
        
        # Check that all methods have display names
        for method in self._methods.keys():
            if method not in self._display_names:
                errors.append(f"Missing display name for method: {method}")
        
        # Check that all methods in language groups exist
        for language, methods in self._language_groups.items():
            for method in methods:
                if method not in self._methods:
                    errors.append(f"Method '{method}' in language '{language}' not found in methods")
        
        # Check that no_case_match methods exist
        for method in self._no_case_match:
            if method not in self._methods:
                errors.append(f"No-case-match method '{method}' not found in methods")
        
        if errors:
            error_msg = "Method registry validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Method registry validated successfully: {len(self._methods)} methods, {len(self._language_groups)} languages")
    
    # Public interface methods
    
    def get_all_methods(self) -> Dict[str, Any]:
        """Get all methods dictionary."""
        return self._methods.copy()
    
    def get_method(self, method_name: str) -> Optional[Any]:
        """Get a specific method module."""
        return self._methods.get(method_name)
    
    def get_method_names(self) -> List[str]:
        """Get list of all method names."""
        return list(self._methods.keys())
    
    def get_languages(self) -> List[str]:
        """Get list of all supported languages."""
        return [UIStrings.SELECT_LANGUAGE] + sorted(self._language_groups.keys())
    
    def get_methods_by_language(self, language: str) -> List[str]:
        """Get methods for a specific language."""
        return self._language_groups.get(language, [])
    
    def get_display_name(self, method_name: str) -> str:
        """Get display name for a method."""
        return self._display_names.get(method_name, method_name)
    
    def get_method_from_display_name(self, display_name: str, language: str) -> str:
        """Get full method name from display name within a language context."""
        if language in self._language_groups:
            for method in self._language_groups[language]:
                if self.get_display_name(method) == display_name:
                    return method
        return display_name
    
    def should_enable_case_match(self, method_name: str) -> bool:
        """Check if a method supports case matching."""
        return method_name not in self._no_case_match
    
    def get_language_code(self, method_name: str) -> str:
        """Get language code for TMX export."""
        return self._method_to_language.get(method_name, 'unknown')
    
    def get_valid_method_names(self) -> Set[str]:
        """Get set of valid method names for validation."""
        return set(self._methods.keys())


# Global registry instance
_registry_instance: Optional[MethodRegistry] = None


def get_method_registry() -> MethodRegistry:
    """Get the global method registry instance (singleton pattern)."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = MethodRegistry()
    return _registry_instance