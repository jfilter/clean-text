"""
Language-specific edge case handling.
"""

import unicodedata

# add new languages here
specials_map = {
    "de": {
        "case_insensitive": [["ä", "ae"], ["ü", "ue"], ["ö", "oe"]],
        "case_sensitive": [["ß", "ss"]],
    },
    "da": {
        "case_insensitive": [["é", "e"], ["Æ", "ae"], ["ø", "oe"], ["å", "aa"]],
        "case_sensitive": [],
    },
    "es": {
        "case_insensitive": [["á", "a"], ["é", "e"], ["í", "i"], ["ó", "o"], ["ú", "u"], ["ñ", "n"]],
        "case_sensitive": [],
    },
    "fo": {
        "case_insensitive": [["á", "a"], ["ð", "d"], ["í", "i"], ["ó", "o"], ["ú", "u"], ["Æ", "ae"], ["ø", "oe"]],
        "case_sensitive": [],
    },
    "fr": {
        "case_insensitive": [
            ["é", "e"],
            ["à", "a"],
            ["è", "e"],
            ["ù", "u"],
            ["â", "a"],
            ["ê", "e"],
            ["î", "oe"],
            ["ô", "o"],
            ["û", "u"],
            ["ë", "e"],
            ["ï", "i"],
            ["ü", "u"],
            ["ÿ", "y"],
            ["ç", "c"],
        ],
        "case_sensitive": [],
    },
    "is": {
        "case_insensitive": [
            ["á", "a"],
            ["ð", "d"],
            ["é", "e"],
            ["í", "i"],
            ["ó", "o"],
            ["ú", "u"],
            ["ý", "y"],
            ["þ", "th"],
            ["Æ", "ae"],
            ["ö", "oe"],
        ],
        "case_sensitive": [],
    },
    "it": {
        "case_insensitive": [
            ["á", "a"],
            ["é", "e"],
            ["í", "i"],
            ["ó", "o"],
            ["ú", "u"],
            ["à", "a"],
            ["è", "e"],
            ["ì", "i"],
            ["ò", "o"],
            ["ù", "u"],
        ],
        "case_sensitive": [],
    },
    "no": {
        "case_insensitive": [
            ["é", "e"],
            ["ó", "o"],
            ["è", "e"],
            ["ò", "o"],
            ["ù", "u"],
            ["ê", "e"],
            ["ô", "o"],
            ["Æ", "ae"],
            ["ø", "oe"],
            ["å", "aa"],
        ],
        "case_sensitive": [],
    },
    "sv": {
        "case_insensitive": [
            ["á", "a"],
            ["é", "e"],
            ["í", "i"],
            ["ó", "o"],
            ["ú", "u"],
            ["è", "e"],
            ["ý", "y"],
            ["ò", "o"],
            ["ù", "u"],
            ["ê", "e"],
            ["ô", "o"],
            ["ð", "d"],
            ["þ", "th"],
            ["Æ", "ae"],
            ["ø", "oe"],
            ["å", "aa"],
            ["ä", "oe"],
            ["ö", "oe"],
        ],
        "case_sensitive": [],
    },
    "se": {
        "case_insensitive": [["å", "aa"], ["ä", "oe"], ["ö", "oe"]],
        "case_sensitive": [],
    },
}
escape_sequence = "xxxxx"


def norm(text):
    return unicodedata.normalize("NFC", text)


def save_replace(text, lang, back=False):
    # perserve the casing of the original text
    # TODO: performance of matching

    # normalize the text to make sure to really match all occurences
    text = norm(text)

    possibilities = (
        specials_map[lang]["case_sensitive"]
        + [[norm(x[0]), x[1]] for x in specials_map[lang]["case_insensitive"]]
        + [[norm(x[0].upper()), x[1].upper()] for x in specials_map[lang]["case_insensitive"]]
    )
    for pattern, target in possibilities:
        if back:
            text = text.replace(escape_sequence + target + escape_sequence, pattern)
        else:
            text = text.replace(pattern, escape_sequence + target + escape_sequence)
    return text
