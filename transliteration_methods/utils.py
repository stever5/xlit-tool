# utils.py
import re
from functools import lru_cache, partial

WORD_SPLIT_PATTERN = re.compile('(\W+)')

def apply_replacements(src_text: str, replacements: dict) -> str:
    """Apply character replacements to source text with error handling."""
    if not isinstance(src_text, str):
        raise TypeError("Source text must be a string")
    if not isinstance(replacements, dict):
        raise TypeError("Replacements must be a dictionary")
    if not replacements:
        return src_text
    
    try:
        # Compile regular expression that matches the substrings to replace
        pattern = re.compile("|".join(map(re.escape, replacements.keys())))
        
        # Use the pattern to replace each match in src_text
        return pattern.sub(lambda match: replacements[match.group(0)], src_text)
    except re.error as e:
        raise ValueError(f"Invalid replacement pattern: {e}")
    except Exception as e:
        raise RuntimeError(f"Error applying replacements: {e}")


# def apply_ordered_replacements(src_text: str, replacements: dict) -> str:
#     # Iterate over replacements. Useful when order of replacement matters.
#     for key, value in replacements.items():
#         src_text = src_text.replace(key, value)
    
#     return src_text


def apply_regex_replacements(src_text: str, replacements: tuple) -> str:
    """Apply regex replacements to source text with error handling."""
    if not isinstance(src_text, str):
        raise TypeError("Source text must be a string")
    if not isinstance(replacements, (tuple, list)):
        raise TypeError("Replacements must be a tuple or list")
    
    try:
        # Iterate over compiled pattern/replacement pairs and replace one by one.
        for pattern, replacement in replacements:
            if not hasattr(pattern, 'sub'):
                raise ValueError("Pattern must be a compiled regex object")
            src_text = pattern.sub(replacement, src_text)
        return src_text
    except Exception as e:
        raise RuntimeError(f"Error applying regex replacements: {e}")


@lru_cache(maxsize=10000)
def translit_word_cm(word: str, translit_method) -> str:
    """Return upper-cased transliteration for upper-cased src_text words."""
    if not isinstance(word, str):
        raise TypeError("Word must be a string")
    if not hasattr(translit_method, 'transliterate'):
        raise AttributeError("Transliteration method must have a 'transliterate' function")
    
    try:
        if word.isupper():
            return translit_method.transliterate(word).upper()
        else:
            return translit_method.transliterate(word)
    except Exception as e:
        raise RuntimeError(f"Error transliterating word '{word}': {e}")


def transliterate_case_match(src_text: str, translit_method) -> str:
    """Return upper-cased transliteration for upper-cased src_text words.
    Used when translit_method sometimes uses digraphs, etc., to represent
    single letters from the src_text in the target string. Wraps the 
    the translit_word_cm function above for efficiency."""
    
    if not isinstance(src_text, str):
        raise TypeError("Source text must be a string")
    if not hasattr(translit_method, 'transliterate'):
        raise AttributeError("Transliteration method must have a 'transliterate' function")
    
    try:
        words = WORD_SPLIT_PATTERN.split(src_text)
        translit_func = partial(translit_word_cm, translit_method=translit_method)
        
        return ''.join([translit_func(word) for word in words])
    except Exception as e:
        raise RuntimeError(f"Error during case-match transliteration: {e}")
