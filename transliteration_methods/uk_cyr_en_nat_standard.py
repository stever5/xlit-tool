# uk_cyr_en_national_standard.py
# Ukrainian to English transliteration per the 2010
# Resolution of the Cabinet of Ministers of Ukraine
import re
from .utils import apply_replacements, apply_regex_replacements

# Special regex patterns for word-beginning cases
regex_patterns = (
    # Handle зг combination to distinguish from ж
    (re.compile(r"Зг"), "Zgh"),
    (re.compile(r"зг"), "zgh"),
    (re.compile(r"ЗГ"), "ZGH"),
    (re.compile(r"зГ"), "zGh"),

    # Word-beginning special cases
    (re.compile(r"\bЄ"), "Ye"),
    (re.compile(r"\bє"), "ye"),
    (re.compile(r"\bЮ"), "Yu"),
    (re.compile(r"\bю"), "yu"),
    (re.compile(r"\bЯ"), "Ya"),
    (re.compile(r"\bя"), "ya"),
    (re.compile(r"\bЇ"), "Yi"),
    (re.compile(r"\bї"), "yi"),
    (re.compile(r"\bЙ"), "Y"),
    (re.compile(r"\bй"), "y"),
)

char_map = {
    "А": "A",
    "а": "a",
    "Б": "B",
    "б": "b",
    "В": "V",
    "в": "v",
    "Г": "H",
    "г": "h",
    "Ґ": "G",
    "ґ": "g",
    "Д": "D",
    "д": "d",
    "Е": "E",
    "е": "e",
    "Є": "Ie",
    "є": "ie",
    "Ж": "Zh",
    "ж": "zh",
    "З": "Z",
    "з": "z",
    "И": "Y",
    "и": "y",
    "І": "I",
    "і": "i",
    "Ї": "I",
    "ї": "i",
    "Й": "I",
    "й": "i",
    "К": "K",
    "к": "k",
    "Л": "L",
    "л": "l",
    "М": "M",
    "м": "m",
    "Н": "N",
    "н": "n",
    "О": "O",
    "о": "o",
    "П": "P",
    "п": "p",
    "Р": "R",
    "р": "r",
    "С": "S",
    "с": "s",
    "Т": "T",
    "т": "t",
    "У": "U",
    "у": "u",
    "Ф": "F",
    "ф": "f",
    "Х": "Kh",
    "х": "kh",
    "Ц": "Ts",
    "ц": "ts",
    "Ч": "Ch",
    "ч": "ch",
    "Ш": "Sh",
    "ш": "sh",
    "Щ": "Shch",
    "щ": "shch",
    "Ь": "",
    "ь": "",
    "Ю": "Iu",
    "ю": "iu",
    "Я": "Ia",
    "я": "ia",
    "'": "",
    "’": "",
}

def transliterate(src_text: str) -> str:
    """Return transliterated string"""
    src_text = apply_regex_replacements(src_text, regex_patterns)
    src_text = apply_replacements(src_text, char_map)
    return src_text
