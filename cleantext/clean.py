"""
Clean your text to create normalized text represenations.
"""

import logging
import re
import unicodedata

from ftfy import fix_text

from . import constants
from .specials import save_replace

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
    """
    Replace strange quotes, i.e., 〞with a single quote ' or a double quote " if it fits better.
    """
    text = constants.SINGLE_QUOTE_REGEX.sub("'", text)
    text = constants.DOUBLE_QUOTE_REGEX.sub('"', text)
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


def to_ascii_unicode(text, lang="en"):
    """
    Try to represent unicode data in ascii characters similar to what a human
    with a US keyboard would choose.
    Works great for languages of Western origin, worse the farther the language
    gets from Latin-based alphabets. It's based on hand-tuned character mappings
    that also contain ascii approximations for symbols and non-Latin alphabets.
    """
    # normalize quotes before since this improves transliteration quality
    text = fix_strange_quotes(text)

    # special handling for German text to preserve umlauts
    if lang == "de":
        text = save_replace(text, lang=lang)

    text = unidecode(text)

    # important to remove utility characters
    if lang == "de":
        text = save_replace(text, lang=lang, back=True)
    return text


def normalize_whitespace(text, no_line_breaks=False):
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more line breaks with a single newline. Also strip leading/trailing whitespace.
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


def replace_digits(text, replace_with="0"):
    """Replace all digits in ``text`` str with ``replace_with`` str, i.e., 123.34 to 000.00"""
    return re.sub(r"\d", replace_with, text)


def replace_currency_symbols(text, replace_with="<CUR>"):
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


def remove_punct(text):
    """
    Replace punctuations from ``text`` with whitespaces.
    Args:
        text (str): raw text
    Returns:
        str
    """
    return text.translate(constants.PUNCT_TRANSLATE_UNICODE)


def clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    no_line_breaks=False,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_numbers=False,
    no_digits=False,
    no_currency_symbols=False,
    no_punct=False,
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    lang="en",
):
    """
    Normalize various aspects of a raw text. A convenience function for applying all other preprocessing functions in one go.
    Args:
        text (str): raw text to preprocess
        fix_unicode (bool): if True, fix "broken" unicode such as
            mojibake and garbled HTML entities
        to_ascii (bool): if True, convert non-to_ascii characters
            into their closest to_ascii equivalents
        lower (bool): if True, all text is lower-cased
        no_line_breaks (bool): if True, strip line breaks from text
        no_urls (bool): if True, replace all URL strings with a special URL token
        no_emails (bool): if True, replace all email strings with a special EMAIL token
        no_phone_numbers (bool): if True, replace all phone number strings
            with a special PHONE token
        no_numbers (bool): if True, replace all number-like strings
            with a special NUMBER token
        no_digits (bool): if True, replace all digits with a special DIGIT token
        no_currency_symbols (bool): if True, replace all currency symbols
            with a special CURRENCY token
        no_punct (bool): if True, remove all punctuation (replace with
            empty string)
        replace_with_url (str): special URL token, default "<URL>",
        replace_with_email (str): special EMAIL token, default "<EMAIL>",
        replace_with_phone_number (str): special PHONE token, default "<PHONE>",
        replace_with_number (str): special NUMBER token, default "<NUMBER>",
        replace_with_digit (str): special DIGIT token, default "0",
        replace_with_currency_symbol (str): special CURRENCY token, default "<CUR>",
        lang (str): special language-depended preprocessing. Besides the default English ('en'), only German ('de') is supported

    Returns:
        str: input ``text`` processed according to function args
    Warning:
        These changes may negatively affect subsequent NLP analysis performed
        on the text, so choose carefully, and preprocess at your own risk!
    """

    if text is None:
        return ''

    text = str(text)

    if fix_unicode:
        text = fix_bad_unicode(text)
    if no_currency_symbols:
        text = replace_currency_symbols(text, replace_with_currency_symbol)
    if to_ascii:
        text = to_ascii_unicode(text, lang=lang)
    if no_urls:
        text = replace_urls(text, replace_with_url)
    if no_emails:
        text = replace_emails(text, replace_with_email)
    if no_phone_numbers:
        text = replace_phone_numbers(text, replace_with_phone_number)
    if no_numbers:
        text = replace_numbers(text, replace_with_number)
    if no_digits:
        text = replace_digits(text, replace_with_digit)
    if no_punct:
        text = remove_punct(text)
    if lower:
        text = text.lower()

    # always normalize whitespace
    text = normalize_whitespace(text, no_line_breaks)

    return text
