"""
Clean your text to create normalized text represenations.
"""

import logging
import os
import re
import sys
from functools import partial
from multiprocessing import Pool
from unicodedata import category

import emoji
from emoji import demojize, emojize
from ftfy import fix_text

from . import constants
from .specials import save_replace, specials_map

log = logging.getLogger()

# fall back to `unicodedata`
try:
    from unidecode import unidecode

except ImportError:
    from unicodedata import normalize

    def unidecode(x):
        return normalize("NFD", x).encode("ASCII", "ignore").decode("utf-8")

    log.warning(
        "Since the GPL-licensed package `unidecode` is not installed, "
        "using Python's `unicodedata` package which yields worse results."
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
    """
    # trying to fix backslash-replaced strings (via https://stackoverflow.com/a/57192592/4028896)
    try:
        text = text.encode("latin", "backslashreplace").decode("unicode-escape")
    except Exception:
        pass

    return fix_text(text, normalization=normalization)


def to_ascii_unicode(text, lang="en", no_emoji=False):
    """
    Try to represent unicode data in ascii characters similar to what a human
    with a US keyboard would choose.
    Works great for languages of Western origin, worse the farther the language
    gets from Latin-based alphabets. It's based on hand-tuned character mappings
    that also contain ascii approximations for symbols and non-Latin alphabets.
    """
    # normalize quotes before since this improves transliteration quality
    text = fix_strange_quotes(text)

    if not no_emoji:
        text = demojize(text, language="alias")

    lang = lang.lower()
    # special handling for German text to preserve umlauts
    if lang in specials_map:
        text = save_replace(text, lang=lang)

    text = unidecode(text)

    # important to remove utility characters
    if lang in specials_map:
        text = save_replace(text, lang=lang, back=True)

    if not no_emoji:
        text = emojize(text, language="alias")

    return text


def normalize_whitespace(text, no_line_breaks=False, strip_lines=True, keep_two_line_breaks=False):
    """
    Given ``text`` str, replace one or more spacings with a single space, and one
    or more line breaks with a single newline. Also strip leading/trailing whitespace.
    """
    if strip_lines:
        text = "\n".join([x.strip() for x in text.splitlines()])

    if no_line_breaks:
        text = constants.MULTI_WHITESPACE_TO_ONE_REGEX.sub(" ", text)
    else:
        if keep_two_line_breaks:
            text = constants.NONBREAKING_SPACE_REGEX.sub(" ", constants.TWO_LINEBREAK_REGEX.sub(r"\n\n", text))
        else:
            text = constants.NONBREAKING_SPACE_REGEX.sub(" ", constants.LINEBREAK_REGEX.sub(r"\n", text))

    return text.strip()


# used below to keep `normalize_whitespace` as a parameter in `clean`
def _normalize_whitespace(*kwargs):
    return normalize_whitespace(*kwargs)


def replace_urls(text, replace_with="<URL>"):
    """
    Replace all URLs in ``text`` str with ``replace_with`` str.
    """
    return constants.URL_REGEX.sub(replace_with, text)


def replace_emails(text, replace_with="<EMAIL>"):
    """
    Replace all emails in ``text`` str with ``replace_with`` str.
    """
    return constants.EMAIL_REGEX.sub(replace_with, text)


def replace_phone_numbers(text, replace_with="<PHONE>"):
    """
    Replace all phone numbers in ``text`` str with ``replace_with`` str.
    """
    return constants.PHONE_REGEX.sub(replace_with, text)


def replace_ip_addresses(text, replace_with="<IP>"):
    """
    Replace all IP addresses in ``text`` str with ``replace_with`` str.
    Supports both IPv4 and IPv6 addresses.
    """
    return constants.IP_REGEX.sub(replace_with, text)


def replace_numbers(text, replace_with="<NUMBER>"):
    """
    Replace all numbers in ``text`` str with ``replace_with`` str.
    """
    return constants.NUMBERS_REGEX.sub(replace_with, text)


def replace_digits(text, replace_with="0"):
    """
    Replace all digits in ``text`` str with ``replace_with`` str, i.e., 123.34 to 000.00
    """
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
    """
    if replace_with is None:
        for k, v in constants.CURRENCIES.items():
            text = text.replace(k, v)
        return text
    else:
        return constants.CURRENCY_REGEX.sub(replace_with, text)


def replace_punct(text, replace_with=" "):
    """
    Replace punctuations from ``text`` with whitespaces (or other tokens).
    """
    return text.translate(
        dict.fromkeys(
            (i for i in range(sys.maxunicode) if category(chr(i)).startswith("P")),
            replace_with,
        )
    )


def remove_punct(text):
    """
    Remove punctuations from ``text``.
    """
    return text.translate(constants.PUNCT_TRANSLATE_UNICODE)


def replace_code(text, replace_with="<CODE>"):
    """
    Replace all code snippets in ``text`` str with ``replace_with`` str.
    Handles both fenced code blocks (triple backtick) and inline code (single backtick).
    """
    return constants.CODE_REGEX.sub(replace_with, text)


def replace_file_paths(text, replace_with="<FILE_PATH>"):
    """
    Replace all file system paths in ``text`` str with ``replace_with`` str.
    Handles Unix paths (/usr/local/bin), Windows paths (C:\\Windows),
    and relative paths (./src, ../lib, ~/Documents).
    """
    return constants.FILE_PATH_REGEX.sub(replace_with, text)


def remove_emoji(text):
    return emoji.replace_emoji(text, replace="")


def _encode_index(n):
    """Encode a non-negative integer as a base-26 lowercase letter string.

    0 → 'a', 1 → 'b', ..., 25 → 'z', 26 → 'ba', 27 → 'bb', ...
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    letters = []
    while True:
        letters.append(chr(ord("a") + n % 26))
        n = n // 26 - 1
        if n < 0:
            break
    return "".join(reversed(letters))


def _protect_exceptions(text, exceptions):
    """Replace regex-matched spans with inert placeholder tokens.

    Returns ``(modified_text, originals)`` where *originals* is a list of
    ``(placeholder, original_text)`` tuples needed by :func:`_restore_exceptions`.
    """
    originals = []
    counter = 0
    for pattern in exceptions:
        compiled = re.compile(pattern)
        matches = list(compiled.finditer(text))
        # replace from back to front so indices stay valid
        for m in reversed(matches):
            placeholder = "zxzexcept" + _encode_index(counter) + "zxz"
            originals.append((placeholder, m.group()))
            text = text[: m.start()] + placeholder + text[m.end() :]
            counter += 1
    return text, originals


def _restore_exceptions(text, originals):
    """Replace placeholder tokens with their original strings."""
    for placeholder, original in originals:
        text = text.replace(placeholder, original)
    return text


def clean(
    text,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    normalize_whitespace=True,
    no_line_breaks=False,
    strip_lines=True,
    keep_two_line_breaks=False,
    no_code=False,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_ip_addresses=False,
    no_file_paths=False,
    no_numbers=False,
    no_digits=False,
    no_currency_symbols=False,
    no_punct=False,
    no_emoji=False,
    replace_with_code="<CODE>",
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_ip_address="<IP>",
    replace_with_file_path="<FILE_PATH>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    replace_with_punct="",
    lang="en",
    exceptions=None,
):
    """
    Normalize various aspects of a raw text. A convenience function for applying all other
    preprocessing functions in one go.
    Args:
        text (str): raw text to preprocess
        fix_unicode (bool): if True, fix "broken" unicode such as
            mojibake and garbled HTML entities
        to_ascii (bool): if True, convert non-to_ascii characters
            into their closest to_ascii equivalents
        lower (bool): if True, all text is lower-cased
        no_line_breaks (bool): if True, strip line breaks from text
        no_code (bool): if True, replace all code snippets (fenced and inline)
            with a special CODE token
        no_urls (bool): if True, replace all URL strings with a special URL token
        no_emails (bool): if True, replace all email strings with a special EMAIL token
        no_phone_numbers (bool): if True, replace all phone number strings
            with a special PHONE token
        no_ip_addresses (bool): if True, replace all IP address strings
            (IPv4 and IPv6) with a special IP token
        no_file_paths (bool): if True, replace all file system paths
            with a special FILE_PATH token
        no_numbers (bool): if True, replace all number-like strings
            with a special NUMBER token
        no_digits (bool): if True, replace all digits with a special DIGIT token
        no_currency_symbols (bool): if True, replace all currency symbols
            with a special CURRENCY token
        no_punct (bool): if True, remove all punctuation (replace with
            empty string)
        replace_with_code (str): special CODE token, default "<CODE>",
        replace_with_url (str): special URL token, default "<URL>",
        replace_with_email (str): special EMAIL token, default "<EMAIL>",
        replace_with_phone_number (str): special PHONE token, default "<PHONE>",
        replace_with_ip_address (str): special IP token, default "<IP>",
        replace_with_file_path (str): special FILE_PATH token, default "<FILE_PATH>",
        replace_with_number (str): special NUMBER token, default "<NUMBER>",
        replace_with_digit (str): special DIGIT token, default "0",
        replace_with_currency_symbol (str): special CURRENCY token, default "<CUR>",
        replace_with_punct (str): replace punctuations with this token, default "",
        lang (str): special language-depended preprocessing.
            Besides the default English ('en'), Danish ('da'), Faroese ('fo'),
            French ('fr'), German ('de'), Icelandic ('is'), Italian ('it'),
            Norwegian ('no'), Scandinavian ('sv'), Spanish ('es'),
            and Swedish ('se') are supported
        exceptions (list[str]): list of regex pattern strings whose matches
            will be preserved verbatim through all cleaning steps.

    Returns:
        str: input ``text`` processed according to function args
    """

    if text is None:
        return ""

    text = str(text)

    text, _exc_originals = _protect_exceptions(text, exceptions or [])

    if fix_unicode:
        text = fix_bad_unicode(text)
    if no_currency_symbols:
        text = replace_currency_symbols(text, replace_with_currency_symbol)
    if no_code:
        text = replace_code(text, replace_with_code)
    if to_ascii:
        text = to_ascii_unicode(text, lang=lang, no_emoji=no_emoji)
    if no_urls:
        text = replace_urls(text, replace_with_url)
    if no_emails:
        text = replace_emails(text, replace_with_email)
    if no_phone_numbers:
        text = replace_phone_numbers(text, replace_with_phone_number)
    if no_ip_addresses:
        text = replace_ip_addresses(text, replace_with_ip_address)
    if no_file_paths:
        text = replace_file_paths(text, replace_with_file_path)
    if no_numbers:
        text = replace_numbers(text, replace_with_number)
    if no_digits:
        text = replace_digits(text, replace_with_digit)
    if no_punct:
        if replace_with_punct == "":
            text = remove_punct(text)
        else:
            text = replace_punct(text, replace_with_punct)

    if no_emoji and not to_ascii:
        text = remove_emoji(text)

    if lower:
        text = text.lower()

    if normalize_whitespace:
        text = _normalize_whitespace(text, no_line_breaks, strip_lines, keep_two_line_breaks)

    text = _restore_exceptions(text, _exc_originals)

    return text


def _resolve_n_jobs(n_jobs):
    """Resolve *n_jobs* into a concrete positive integer (number of workers).

    * ``None`` or ``1`` → 1 (sequential, no multiprocessing overhead)
    * ``-1``            → ``os.cpu_count()`` (all cores)
    * ``-N`` (N > 1)    → ``max(1, cpu_count + 1 + n_jobs)``
    * ``0``             → raises ``ValueError``
    * positive int      → used as-is
    """
    if n_jobs is None:
        return 1
    if not isinstance(n_jobs, int):
        raise TypeError(f"n_jobs must be an integer or None, got {type(n_jobs).__name__}")
    if n_jobs == 0:
        raise ValueError("n_jobs must not be 0")
    if n_jobs < 0:
        cpu_count = os.cpu_count() or 1
        if n_jobs == -1:
            return cpu_count
        return max(1, cpu_count + 1 + n_jobs)
    return n_jobs


def clean_texts(
    texts,
    n_jobs=1,
    *,
    fix_unicode=True,
    to_ascii=True,
    lower=True,
    normalize_whitespace=True,
    no_line_breaks=False,
    strip_lines=True,
    keep_two_line_breaks=False,
    no_code=False,
    no_urls=False,
    no_emails=False,
    no_phone_numbers=False,
    no_ip_addresses=False,
    no_file_paths=False,
    no_numbers=False,
    no_digits=False,
    no_currency_symbols=False,
    no_punct=False,
    no_emoji=False,
    replace_with_code="<CODE>",
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_ip_address="<IP>",
    replace_with_file_path="<FILE_PATH>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    replace_with_punct="",
    lang="en",
    exceptions=None,
):
    """Clean a list of texts, optionally in parallel using multiprocessing.

    Args:
        texts: iterable of strings to clean.
        n_jobs: number of parallel workers.
            ``1`` or ``None`` for sequential processing (default),
            ``-1`` to use all available CPU cores,
            any positive int for that many workers.
        **kwargs: all remaining keyword arguments are forwarded to
            :func:`clean` unchanged.

    Returns:
        list[str]: cleaned texts in the same order as *texts*.
    """
    texts = list(texts)
    n_jobs = _resolve_n_jobs(n_jobs)

    kwargs = dict(
        fix_unicode=fix_unicode,
        to_ascii=to_ascii,
        lower=lower,
        normalize_whitespace=normalize_whitespace,
        no_line_breaks=no_line_breaks,
        strip_lines=strip_lines,
        keep_two_line_breaks=keep_two_line_breaks,
        no_code=no_code,
        no_urls=no_urls,
        no_emails=no_emails,
        no_phone_numbers=no_phone_numbers,
        no_ip_addresses=no_ip_addresses,
        no_file_paths=no_file_paths,
        no_numbers=no_numbers,
        no_digits=no_digits,
        no_currency_symbols=no_currency_symbols,
        no_punct=no_punct,
        no_emoji=no_emoji,
        replace_with_code=replace_with_code,
        replace_with_url=replace_with_url,
        replace_with_email=replace_with_email,
        replace_with_phone_number=replace_with_phone_number,
        replace_with_ip_address=replace_with_ip_address,
        replace_with_file_path=replace_with_file_path,
        replace_with_number=replace_with_number,
        replace_with_digit=replace_with_digit,
        replace_with_currency_symbol=replace_with_currency_symbol,
        replace_with_punct=replace_with_punct,
        lang=lang,
        exceptions=exceptions,
    )

    worker = partial(clean, **kwargs)

    if n_jobs == 1 or len(texts) == 0:
        return [worker(t) for t in texts]

    with Pool(processes=min(n_jobs, len(texts))) as pool:
        return pool.map(worker, texts)
