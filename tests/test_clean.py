import pytest

import cleantext


def test_normalize_whitespace():
    text = "Hello, world!  Hello...\t \tworld?\n\nHello:\r\n\n\nWorld. "
    proc_text = "Hello, world! Hello... world?\nHello:\nWorld."
    assert cleantext.normalize_whitespace(text) == proc_text


def test_unpack_contractions():
    text = "Y'all can't believe you're not who they've said I'll become, but shouldn't."
    proc_text = "You all can not believe you are not who they have said I will become, but should not."
    assert cleantext.unpack_contractions(text) == proc_text


def test_replace_urls():
    text = "I learned everything I know from www.stackoverflow.com and http://wikipedia.org/ and Mom."
    proc_text = "I learned everything I know from *URL* and *URL* and Mom."
    assert cleantext.replace_urls(text, "*URL*") == proc_text


def test_replace_emails():
    text = "I can be reached at username@example.com through next Friday."
    proc_text = "I can be reached at *EMAIL* through next Friday."
    assert cleantext.replace_emails(text, "*EMAIL*") == proc_text


def test_replace_phone_numbers():
    text = "I can be reached at 555-123-4567 through next Friday."
    proc_text = "I can be reached at *PHONE* through next Friday."
    assert cleantext.replace_phone_numbers(text, "*PHONE*") == proc_text


def test_replace_numbers():
    text = "I owe $1,000.99 to 123 people for 2 +1 reasons."
    proc_text = "I owe $*NUM* to *NUM* people for *NUM* *NUM* reasons."
    assert cleantext.replace_numbers(text, "*NUM*") == proc_text


def test_remove_punct():
    text = "I can't. No, I won't! It's a matter of \"principle\"; of -- what's the word? -- conscience."
    proc_text = "I can t  No  I won t  It s a matter of  principle   of    what s the word     conscience "
    assert cleantext.remove_punct(text) == proc_text


def test_remove_punct_marks():
    text = "I can't. No, I won't! It's a matter of \"principle\"; of -- what's the word? -- conscience."
    proc_text = "I can t. No, I won t! It s a matter of  principle ; of   what s the word?   conscience."
    assert cleantext.remove_punct(text, marks="-'\"") == proc_text


def test_replace_currency_symbols():
    tests = [
        (
            "$1.00 equals £0.67 equals €0.91.",
            "USD1.00 equals GBP0.67 equals EUR0.91.",
            "*CUR* 1.00 equals *CUR* 0.67 equals *CUR* 0.91.",
        ),
        (
            "this zebra costs $100.",
            "this zebra costs USD100.",
            "this zebra costs *CUR* 100.",
        ),
    ]
    for text, proc_text1, proc_text2 in tests:
        assert cleantext.replace_currency_symbols(text, replace_with=None) == proc_text1
        assert (
            cleantext.replace_currency_symbols(text, replace_with="*CUR* ")
            == proc_text2
        )


def test_remove_accents():
    text = "El niño se asustó -- qué miedo!"
    proc_text = "El nino se asusto -- que miedo!"
    assert cleantext.remove_accents(text, method="unicode") == proc_text
    assert cleantext.remove_accents(text, method="ascii") == proc_text
    with pytest.raises(Exception):
        _ = cleantext.remove_accents(text, method="foo")


def text_to_ascii_unicode():
    text = (
        "and install a \\u2018new\\u2019 society in their"
    )  # and install a ‘new’ society in their
    assert cleantext.fix_bad_unicode(text) == "and install a 'new' society in their"


def test_zero_digits():
    text = "in the 1970s there was 12.3 and 111 11 33"
    assert cleantext.zero_digits(text) == "in the 1970s there was 00.0 and 000 00 00"
