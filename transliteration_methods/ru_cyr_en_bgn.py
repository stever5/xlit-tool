# ru_cyr_en_bgn.py
import re
from .utils import apply_replacements, apply_regex_replacements

regex_patterns = (
    (re.compile(r"([бвгджзклмнпрстфхцчшщБВГДЖЗКЛМНПРСТФХЦЧШЩ])е"), r"\1e"),
    (re.compile(r"([бвгджзклмнпрстфхцчшщБВГДЖЗКЛМНПРСТФХЦЧШЩ])Е"), r"\1E"),
    (re.compile(r"([бвгджзклмнпрстфхцчшщБВГДЖЗКЛМНПРСТФХЦЧШЩ])ё"), r"\1ë"),
    (re.compile(r"([бвгджзклмнпрстфхцчшщБВГДЖЗКЛМНПРСТФХЦЧШЩ])Ё"), r"\1Ë"),
)

# Do replacements after handling regex replacements
char_map = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'ye',
    'ё': 'yë',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': '”',
    'ы': 'y',
    'ь': '’',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'Ye',
    'Ё': 'Yë',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'Kh',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ъ': '”',
    'Ы': 'Y',
    'Ь': '’',
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya'
}

def transliterate(src_text: str) -> str:
    """Return transliterated string"""
    src_text = apply_regex_replacements(src_text, regex_patterns)
    src_text = apply_replacements(src_text, char_map)
    return src_text
