"""
Generic text processing functions.
"""


def remove_substrings(text, to_replace, replace_with=""):
    """
    Remove (or replace) substrings from a text.
    Args:
        text (str): raw text to preprocess
        to_replace (iterable or str): substrings to remove/replace
        replace_with (str): defaults to an empty string but
            you replace substrings with a token.
    """
    if isinstance(to_replace, str):
        to_replace = [to_replace]

    result = text
    for x in to_replace:
        result = result.replace(x, replace_with)
    return result
