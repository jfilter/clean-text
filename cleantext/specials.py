import unicodedata

# add new languages here
specials = {
    "de": {
        "case_insensitive": [["ä", "ae"], ["ü", "ue"], ["ö", "oe"]],
        "case_sensitive": [["ß", "ss"]],
    }
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
        specials[lang]["case_sensitive"]
        + [[norm(x[0]), x[1]] for x in specials[lang]["case_insensitive"]]
        + [
            [norm(x[0].upper()), x[1].upper()]
            for x in specials[lang]["case_insensitive"]
        ]
    )
    for pattern, target in possibilities:
        if back:
            text = text.replace(escape_sequence + target + escape_sequence, pattern)
        else:
            text = text.replace(pattern, escape_sequence + target + escape_sequence)
    return text
