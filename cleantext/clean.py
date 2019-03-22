"""

"""

import logging
import re
import unicodedata

from ftfy import fix_text

from . import constants

log = logging.getLogger()

# fall back to `unicodedata`
try:
    from unidecode import unidecode
except:
    from unicodedata import normalize

    unidecode = lambda x: normalize("NFKD", x)
    log.warning(
        "Since the GPL-licensed package `unidecode` is not installed, using Python's `unicodedata` package which yields worse results."
    )


def fix_strange_quotes(text):
    text = constants.SINGLE_QUOTE_REGEX.sub("'", text)
    text = constants.SINGLE_QUOTE_REGEX.sub('"', text)
    return text


def fix_bad_unicode(text, normalization="NFC"):
    """
    Fix unicode text that's "broken" using `ftfy <http://ftfy.readthedocs.org/>`_;
    this includes mojibake, HTML entities and other code cruft,
    and non-standard forms for display purposes.
    Args:
        text (str): raw text
        normalization ({'NFC', 'NFKC', 'NFD', 'NFKD'}): if 'NFC',
            combines characters and diacritics written using separate code points,
            e.g. converting "e" plus an acute accent modifier into "é"; unicode
            can be converted to NFC form without any change in its meaning!
            if 'NFKC', additional normalizations are applied that can change
            the meanings of characters, e.g. ellipsis characters will be replaced
            with three periods
    Returns:
        str
    """
    # fix if the unicode is fucked up
    try:
        text = text.encode().decode("unicode-escape")
    except:
        pass

    return fix_text(text, normalization=normalization)


def to_ascii_unicode(text):
    """
    Try to represent unicode data in ascii characters similar to what a human
    with a US keyboard would choose.
    Works great for languages of Western origin, worse the farther the language
    gets from Latin-based alphabets. It's based on hand-tuned character mappings
    that also contain ascii approximations for symbols and non-Latin alphabets.
    """

    # normalize quotes before
    text = fix_strange_quotes(text)

    return unidecode(text)


def normalize_whitespace(text, no_line_breaks):
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more linebreaks with a single newline. Also strip leading/trailing whitespace.
    """
    if no_line_breaks:
        text = constants.MULTI_WHITESPACE_TO_ONE_REGEX.sub(" ", text)
    else:
        text = constants.NONBREAKING_SPACE_REGEX.sub(
            " ", constants.LINEBREAK_REGEX.sub(r"\n", text)
        )
    return text.strip()


def replace_urls(text, replace_with="<URL>"):
    """Replace all URLs in ``text`` str with ``replace_with`` str."""
    # return constants.URL_REGEX.sub(
    #     replace_with, constants.SHORT_URL_REGEX.sub(replace_with, text)
    # )
    return constants.URL_REGEX.sub(replace_with, text)


def replace_emails(text, replace_with="<EMAIL>"):
    """Replace all emails in ``text`` str with ``replace_with`` str."""
    return constants.EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with="<PHONE>"):
    """Replace all phone numbers in ``text`` str with ``replace_with`` str."""
    return constants.PHONE_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with="<NUMBER>"):
    """Replace all numbers in ``text`` str with ``replace_with`` str."""
    return constants.NUMBERS_REGEX.sub(replace_with, text)


def to_zero_digits(text):
    """
    All digits are reduced to 0. 123.34 to 000.00
    """
    return re.sub(r"\d", "0", text)


def replace_currency_symbols(text, replace_with=None):
    """
    Replace all currency symbols in ``text`` str with string specified by ``replace_with`` str.
    Args:
        text (str): raw text
        replace_with (str): if None (default), replace symbols with
            their standard 3-letter abbreviations (e.g. '$' with 'USD', '£' with 'GBP');
            otherwise, pass in a string with which to replace all symbols
            (e.g. "*CURRENCY*")
    Returns:
        str
    """
    if replace_with is None:
        for k, v in constants.CURRENCIES.items():
            text = text.replace(k, v)
        return text
    else:
        return constants.CURRENCY_REGEX.sub(replace_with, text)


def remove_punct(text, marks=None):
    """
    Remove punctuation from ``text`` by replacing all instances of ``marks``
    with whitespace.
    Args:
        text (str): raw text
        marks (str): If specified, remove only the characters in this string,
            e.g. ``marks=',;:'`` removes commas, semi-colons, and colons.
            Otherwise, all punctuation marks are removed.
    Returns:
        str
    Note:
        When ``marks=None``, Python's built-in :meth:`str.translate()` is
        used to remove punctuation; otherwise, a regular expression is used
        instead. The former's performance is about 5-10x faster.
    """
    if marks:
        return re.sub("[{}]+".format(re.escape(marks)), " ", text, flags=re.UNICODE)
    else:
        return text.translate(constants.PUNCT_TRANSLATE_UNICODE)


def clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_numbers=False,
    zero_digits=False,
    no_currency_symbols=False,
    no_punct=False,
    no_line_breaks=False,
):
    """
    Normalize various aspects of a raw text doc before parsing it with Spacy.
    A convenience function for applying all other preprocessing functions in one go.
    Args:
        text (str): raw text to preprocess
        fix_unicode (bool): if True, fix "broken" unicode such as
            mojibake and garbled HTML entities
        lower (bool): if True, all text is lower-cased
        to_ascii (bool): if True, convert non-to_ascii characters
            into their closest to_ascii equivalents
        no_urls (bool): if True, replace all URL strings with '*URL*'
        no_emails (bool): if True, replace all email strings with '*EMAIL*'
        no_phone_numbers (bool): if True, replace all phone number strings
            with '*PHONE*'
        no_numbers (bool): if True, replace all number-like strings
            with '*NUMBER*'
        no_currency_symbols (bool): if True, replace all currency symbols
            with their standard 3-letter abbreviations
        no_punct (bool): if True, remove all punctuation (replace with
            empty string)
    Returns:
        str: input ``text`` processed according to function args
    Warning:
        These changes may negatively affect subsequent NLP analysis performed
        on the text, so choose carefully, and preprocess at your own risk!
    """
    text = str(text)
    if fix_unicode is True:
        text = fix_bad_unicode(text, normalization="NFC")
    if no_currency_symbols is True:
        text = replace_currency_symbols(text)
    if to_ascii is True:
        text = to_ascii_unicode(text)
    if no_urls is True:
        text = replace_urls(text)
    if no_emails is True:
        text = replace_emails(text)
    if no_phone_numbers is True:
        text = replace_phone_numbers(text)
    if no_numbers is True:
        text = replace_numbers(text)
    if zero_digits:
        text = to_zero_digits(text)
    if no_punct is True:
        text = remove_punct(text)
    if lower is True:
        text = text.lower()
    # always normalize whitespace
    text = normalize_whitespace(text, no_line_breaks)

    return text
