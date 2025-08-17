# GOST 7.79-2000 System B
import re
from .utils import apply_replacements, apply_regex_replacements

char_map = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'j',
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
    'х': 'x',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shh',
    'ъ': '``',
    'ы': 'y`',
    'ь': '`',
    'э': 'e`',
    'ю': 'yu',
    'я': 'ya',
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Yo',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'J',
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
    'Х': 'X',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shh',
    'Ъ': '``',
    'Ы': 'Y`',
    'Ь': '`',
    'Э': 'E`',
    'Ю': 'Yu',
    'Я': 'Ya',
}

# To handle цЦ.
regex_patterns = (
    (re.compile(r'ц([ieyjIEYJ])'), r'c\1'),
    (re.compile(r'Ц([ieyjIEYJ])'), r'C\1'),
    (re.compile('ц'), 'cz'),
    (re.compile('Ц'), 'Cz'),
)

def transliterate(src_text: str) -> str:
    """Return transliterated string"""
    src_text = apply_replacements(src_text, char_map)
    src_text = apply_regex_replacements(src_text, regex_patterns)
    return src_text

