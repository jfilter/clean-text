import pytest

import cleantext


def test_normalize_whitespace():
    text = "Hello, world!  Hello...\t \tworld?\n\nHello:\r\n\n\nWorld. "
    proc_text = "Hello, world! Hello... world?\nHello:\nWorld."
    assert cleantext.normalize_whitespace(text, no_line_breaks=False) == proc_text
    assert cleantext.normalize_whitespace(" dd\nd  ", no_line_breaks=True) == "dd d"


def test_replace_urls():
    texts = [
        [
            "I learned everything I know from www.stackoverflow.com and http://wikipedia.org/ and Mom.",
            "I learned everything I know from *URL* and *URL* and Mom.",
        ],
        [
            "There's a bunch of references in that one scene alone, including [Moana](https://en.wikipedia.org/wiki/Moana_%282016_film%29), which comes out later this year.",
            "There's a bunch of references in that one scene alone, including [Moana](*URL*), which comes out later this year.",
        ],
        [
            "Also this should be fixed http://localhost:8080, https://localhost:8080, localhost:8080",
            "Also this should be fixed *URL*, *URL*, localhost:8080",
        ],
    ]

    for text, proc_text in texts:
        assert cleantext.replace_urls(text, "*URL*") == proc_text


email_addresses = [
    "mustermann@fh-aachen.de",
    "mustermann(at)fh-aachen.de",
    "m.mustermann@fh-aachen.de",
    "m.mustermann(at)fh-aachen.de",
    "m.mustermann<at>fh-aachen.de",
    "m.mustermann[at]fh-aachen.de",
    "m.mustermann{at}fh-aachen.de",
    "m.mustermann@alumni.fh-aachen.de",
    "max.mustermann@alumni.fh-aachen.com",
    "hotbunny1337@test.mail.gg",
    "test@this.really.should.work.com",
]

not_email_addresses = [
    "mustermann@ fh-aachen.de",
    "mustermannatfh-aachen.de",
    "mustermannat)fh-aachen.de",
    "@test.de",
    "hu@.de",
]


def test_replace_emails():
    text = "I can be reached at username@example.com through next Friday."
    proc_text = "I can be reached at *EMAIL* through next Friday."
    assert cleantext.replace_emails(text, "*EMAIL*") == proc_text


def test_email_addresses():
    for x in email_addresses:
        assert cleantext.replace_emails(x, "*EMAIL*") == "*EMAIL*"


def test_not_email_addresses():
    for x in not_email_addresses:
        assert cleantext.replace_emails(x, "*EMAIL*") != "*EMAIL*"


phone_numbers = [
    "+49 123 1548690",
    "555-123-4567",
    "2404 9099130",
    "024049099130",
    "02404 9099130",
    "02404/9099130",
    "+492404 9099130",
    "+4924049099130",
    "+492404/9099130",
    "0160 123456789",
    "0160/123456789",
    "+32160 123456789",
    "Tel.: 0160 123456789",
    "001-504-724-7835x2050",
    "001-687-915-1144",
    "001-507-783-9793x4107",
]


def test_replace_phone_numbers():
    for x in phone_numbers:
        x_phone = cleantext.replace_phone_numbers(x, "*PHONE*")
        assert "PHONE" in x_phone and not any(map(str.isdigit, x_phone)), x + " / " + x_phone


ipv4_addresses = [
    "192.168.1.1",
    "10.0.0.1",
    "255.255.255.0",
    "8.8.8.8",
    "172.16.0.1",
    "127.0.0.1",
    "0.0.0.0",
]

ipv6_addresses = [
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "2001:db8:85a3::8a2e:370:7334",
    "::1",
    "::",
    "fe80::1",
    "::ffff:192.168.1.1",
]

not_ip_addresses = [
    "999.999.999.999",
    "256.1.1.1",
    "1.2.3",
    "1.2.3.4.5",
]


def test_replace_ip_addresses():
    for x in ipv4_addresses:
        result = cleantext.replace_ip_addresses(x, "*IP*")
        assert result == "*IP*", f"{x} -> {result}"


def test_replace_ipv6_addresses():
    for x in ipv6_addresses:
        result = cleantext.replace_ip_addresses(x, "*IP*")
        assert "*IP*" in result, f"{x} -> {result}"


def test_not_ip_addresses():
    for x in not_ip_addresses:
        result = cleantext.replace_ip_addresses(x, "*IP*")
        assert result != "*IP*", f"{x} should not be matched but got {result}"


def test_replace_ip_in_text():
    text = "The server at 192.168.1.1 is down and 10.0.0.1 is unreachable."
    proc_text = "The server at *IP* is down and *IP* is unreachable."
    assert cleantext.replace_ip_addresses(text, "*IP*") == proc_text


def test_replace_ip_clean():
    text = "Connect to 192.168.1.1 now"
    assert "ip" in cleantext.clean(text, no_ip_addresses=True).lower()


def test_replace_numbers():
    text = "I owe $1,000.99 to 123 peo4ple for 2 +1 reasons."
    proc_text = "I owe $*NUM* to *NUM* peo*NUM*ple for *NUM* *NUM* reasons."
    assert cleantext.replace_numbers(text, "*NUM*") == proc_text


def test_remove_punct():
    text = "I can't. No, I won't! It's a matter of \"principle\"; of -- what's the word? -- conscience."
    proc_text = "I cant No I wont Its a matter of principle of  whats the word  conscience"
    assert cleantext.remove_punct(text) == proc_text


def test_replace_punct():
    text = "I can't. No, I won't!"
    proc_text = "i can t no i won t"
    assert cleantext.clean(text, no_punct=True, replace_with_punct=" ") == proc_text


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
        assert cleantext.replace_currency_symbols(text, replace_with="*CUR* ") == proc_text2


def test_fix_bad_unicode():
    text = "and install a \\u2018new\\u2019 society in their"  # and install a ‘new’ society in their
    assert cleantext.fix_bad_unicode(text) == "and install a 'new' society in their"

    assert "všetko" == cleantext.fix_bad_unicode("všetko")
    assert "Všetko" == cleantext.fix_bad_unicode("Všetko")


def test_zero_digits():
    text = "in the 1970s there was 12.3 and 111 11 33 $23 03 wins"
    assert cleantext.replace_digits(text) == "in the 0000s there was 00.0 and 000 00 00 $00 00 wins"

    text = "7 Golf Records More 'Unbreakable' Than the Warriors' 73 Wins"
    assert cleantext.replace_digits(text) == "0 Golf Records More 'Unbreakable' Than the Warriors' 00 Wins"


def test_to_ascii():
    assert cleantext.to_ascii_unicode("whatëver") == "whatever"
    assert cleantext.to_ascii_unicode("Äpfel»", lang="de") == 'Äpfel"'
    assert cleantext.to_ascii_unicode("Äpfel»", lang="DE") == 'Äpfel"'


def test_whitespace():
    assert cleantext.clean(" peter", normalize_whitespace=False) == " peter"
    assert cleantext.clean(" peter", normalize_whitespace=True) == "peter"
    assert cleantext.clean(" pet\n\ner", normalize_whitespace=True, no_line_breaks=True) == "pet er"
    assert cleantext.clean(" pet\n\ner", normalize_whitespace=True, no_line_breaks=False) == "pet\ner"


emoji_line = "🤔 🙈 me, se 😌 ds 💕👭👙 hello 👩🏾‍🎓 emoji hello 👨‍👩‍👦‍👦 how are 😊 you today🙅🏽🙅🏽"


def test_keep_emojis():
    assert cleantext.clean(emoji_line) == emoji_line


def test_remove_emojis():
    assert cleantext.clean(emoji_line, no_emoji=True) == "me, se ds hello emoji hello how are you today"


def test_remove_emojis_no_ascii():
    assert cleantext.clean("😊 you today🙅🏽🙅🏽", to_ascii=False, no_emoji=True) == "you today"


def test_remove_single_emoji():
    assert cleantext.remove_emoji("Hello 👋 world") == "Hello  world"


def test_remove_emoji_only_string():
    assert cleantext.remove_emoji("🎉🎊🎈") == ""


def test_remove_emoji_no_emoji_input():
    assert cleantext.remove_emoji("no emoji here") == "no emoji here"


def test_remove_emoji_skin_tone_variants():
    assert cleantext.remove_emoji("hi 👍🏻👍🏽👍🏿 there") == "hi  there"


def test_remove_emoji_zwj_sequences():
    # Zero-width joiner sequences like family emoji
    assert cleantext.remove_emoji("family: 👨‍👩‍👧‍👦 end") == "family:  end"


def test_demojize_roundtrip():
    """Verify demojize/emojize with language='alias' round-trips correctly."""
    text_with_emoji = "Hello 😊 world 🌍"
    demojized = cleantext.to_ascii_unicode(text_with_emoji, no_emoji=False)
    # Should preserve emoji through demojize -> unidecode -> emojize cycle
    assert "😊" in demojized or ":)" in demojized or "smiling" in demojized


def test_replace_code_fenced_block():
    text = "Here is code:\n```python\nprint('hello')\n```\nEnd."
    assert cleantext.replace_code(text, "*CODE*") == "Here is code:\n*CODE*\nEnd."


def test_replace_code_fenced_block_no_lang():
    text = "Before\n```\nsome code\n```\nAfter"
    assert cleantext.replace_code(text, "*CODE*") == "Before\n*CODE*\nAfter"


def test_replace_code_inline():
    text = "Use `print()` to output text."
    assert cleantext.replace_code(text, "*CODE*") == "Use *CODE* to output text."


def test_replace_code_multiple_inline():
    text = "Both `foo` and `bar` are variables."
    assert cleantext.replace_code(text, "*CODE*") == "Both *CODE* and *CODE* are variables."


def test_replace_code_empty_backticks():
    text = "This is `` not code."
    assert cleantext.replace_code(text, "*CODE*") == "This is `` not code."


def test_replace_code_preserves_regular_text():
    text = "No code here, just regular text."
    assert cleantext.replace_code(text, "*CODE*") == text


file_paths = [
    "/usr/local/bin",
    "/etc/nginx/nginx.conf",
    "/home/user/Documents/file.txt",
    "C:\\Windows\\System32",
    "C:\\Users\\Name\\file.txt",
    "D:\\projects\\src\\main.py",
    "./src/main.py",
    "../lib/utils.js",
    "~/Documents/notes.md",
    "~/.config/settings.json",
]

not_file_paths = [
    "hello/world",
    "/s",
]


def test_replace_file_paths():
    for path in file_paths:
        result = cleantext.replace_file_paths(path, "*PATH*")
        assert result == "*PATH*", f"Failed for: {path} -> {result}"


def test_not_file_paths():
    for path in not_file_paths:
        result = cleantext.replace_file_paths(path, "*PATH*")
        assert result != "*PATH*", f"False positive for: {path} -> {result}"


def test_replace_file_paths_in_sentence():
    text = "Edit the file at /etc/config.yaml and restart."
    proc_text = "Edit the file at *PATH* and restart."
    assert cleantext.replace_file_paths(text, "*PATH*") == proc_text


def test_replace_windows_path_in_sentence():
    text = "Open C:\\Users\\Admin\\Desktop\\report.pdf to view."
    proc_text = "Open *PATH* to view."
    assert cleantext.replace_file_paths(text, "*PATH*") == proc_text


def test_replace_file_paths_preserves_regular_text():
    text = "No paths here, just regular text."
    assert cleantext.replace_file_paths(text, "*PATH*") == text


def test_clean_no_code():
    text = "Use `foo()` here."
    result = cleantext.clean(text, no_code=True, lower=False, to_ascii=False, fix_unicode=False)
    assert "`foo()`" not in result
    assert "<CODE>" in result


def test_clean_no_file_paths():
    text = "Edit /etc/nginx/nginx.conf now."
    result = cleantext.clean(text, no_file_paths=True, lower=False, to_ascii=False, fix_unicode=False)
    assert "/etc/nginx/nginx.conf" not in result
    assert "<FILE_PATH>" in result


def test_clean_code_before_urls():
    text = "See:\n```\nhttp://example.com\n```\nEnd."
    result = cleantext.clean(text, no_code=True, no_urls=True, lower=False, to_ascii=False, fix_unicode=False)
    assert "<URL>" not in result
    assert "<CODE>" in result


def test_remove_trail_leading_whitespace():
    text_input = """
    Sehr geehrte Damen und Herren,

ich möchte Sie bitten, zu folgendem Fall Stellung zu nehmen. Ich habe einen Fotoautomaten für biometrische Passfotos benutzt, der mein Gesicht nicht erkannt hat. Es besteht die Vermutung, dass dieser Fotoautomat vom BSI zertifiziert ist (Zertifikat BSI-DSZ-CC-0985-2018).

Der Fotoautomat steht in  19061  Berlin.



		Marke: Fotofix





		Ort des Automats: Bezirksamt / Bürgeramt / Bürgerbüro





Mit freundlichen Grüßen,
Johannes dfdfd
    """

    text_output = """Sehr geehrte Damen und Herren,

ich möchte Sie bitten, zu folgendem Fall Stellung zu nehmen. Ich habe einen Fotoautomaten für biometrische Passfotos benutzt, der mein Gesicht nicht erkannt hat. Es besteht die Vermutung, dass dieser Fotoautomat vom BSI zertifiziert ist (Zertifikat BSI-DSZ-CC-0985-2018).

Der Fotoautomat steht in 19061 Berlin.

Marke: Fotofix

Ort des Automats: Bezirksamt / Bürgeramt / Bürgerbüro

Mit freundlichen Grüßen,
Johannes dfdfd"""

    print(
        cleantext.clean(
            text_input,
            lower=False,
            lang="de",
            no_line_breaks=False,
            keep_two_line_breaks=True,
        )
    )

    assert text_output == cleantext.clean(
        text_input,
        lower=False,
        lang="de",
        no_line_breaks=False,
        keep_two_line_breaks=True,
    )


def test_remove_trail_leading_whitespace_bytes():
    text_input = b"Sehr geehrte Damen und Herren,\\r\\n\\r\\nich m\\xf6chte Sie bitten, zu folgendem Fall Stellung zu nehmen. Ich habe einen Fotoautomaten f\\xfcr biometrische Passfotos benutzt, der mein Gesicht nicht erkannt hat. Es besteht die Vermutung, dass dieser Fotoautomat vom BSI zertifiziert ist (Zertifikat BSI-DSZ-CC-0985-2018).\\r\\n\\r\\nDer Fotoautomat steht in  .\\r\\n\\r\\n\\r\\n\\t\\r\\n\\t\\tOrt des Automats: \\r\\n\\t\\r\\n\\r\\n\\r\\n\\r\\n \\r\\n\\t\\r\\n\\t\\tMarke: \\r\\n\\t\\r\\n\\r\\n\\r\\n\\r\\n\\r\\nHier noch Text von Anna Lena.\\r\\n\\r\\nMit freundlichen Gr\\xfc\\xdfen"
    text_input = text_input.decode("unicode_escape")
    text_output = """Sehr geehrte Damen und Herren,

ich möchte Sie bitten, zu folgendem Fall Stellung zu nehmen. Ich habe einen Fotoautomaten für biometrische Passfotos benutzt, der mein Gesicht nicht erkannt hat. Es besteht die Vermutung, dass dieser Fotoautomat vom BSI zertifiziert ist (Zertifikat BSI-DSZ-CC-0985-2018).

Der Fotoautomat steht in .

Ort des Automats:

Marke:

Hier noch Text von Anna Lena.

Mit freundlichen Grüßen"""

    print(
        cleantext.clean(
            text_input,
            lower=False,
            lang="de",
            no_line_breaks=False,
            keep_two_line_breaks=True,
        )
    )

    assert text_output == cleantext.clean(
        text_input,
        lower=False,
        lang="de",
        no_line_breaks=False,
        keep_two_line_breaks=True,
    )


# ---------------------------------------------------------------------------
# clean_texts tests
# ---------------------------------------------------------------------------


def test_clean_texts_basic():
    texts = ["Hello, World!", "Foo   Bar"]
    result = cleantext.clean_texts(texts)
    assert result == [cleantext.clean(t) for t in texts]


def test_clean_texts_empty_list():
    assert cleantext.clean_texts([]) == []


def test_clean_texts_single_item():
    result = cleantext.clean_texts(["Hello!"])
    assert result == [cleantext.clean("Hello!")]


def test_clean_texts_order_preserved():
    texts = ["z text", "a text", "m text"]
    result = cleantext.clean_texts(texts, n_jobs=2)
    assert result == [cleantext.clean(t) for t in texts]


def test_clean_texts_kwargs_passthrough():
    texts = ["Visit http://example.com", "Straße in München"]
    result = cleantext.clean_texts(texts, no_urls=True, lang="de")
    expected = [cleantext.clean(t, no_urls=True, lang="de") for t in texts]
    assert result == expected


def test_clean_texts_n_jobs_none():
    texts = ["hello", "world"]
    result = cleantext.clean_texts(texts, n_jobs=None)
    assert result == [cleantext.clean(t) for t in texts]


def test_clean_texts_n_jobs_minus_one():
    texts = ["hello", "world", "foo"]
    result = cleantext.clean_texts(texts, n_jobs=-1)
    assert result == [cleantext.clean(t) for t in texts]


def test_clean_texts_n_jobs_zero():
    with pytest.raises(ValueError):
        cleantext.clean_texts(["hello"], n_jobs=0)


def test_clean_texts_n_jobs_exceeds_len():
    texts = ["hello", "world"]
    result = cleantext.clean_texts(texts, n_jobs=100)
    assert result == [cleantext.clean(t) for t in texts]


def test_clean_texts_parallel_matches_sequential():
    texts = [
        "Hello World!",
        "Visit http://example.com today",
        "Price is $100",
        None,
        "Äpfel und Birnen",
    ]
    seq = cleantext.clean_texts(texts, n_jobs=1)
    par = cleantext.clean_texts(texts, n_jobs=2)
    assert seq == par


def test_clean_texts_none_items():
    result = cleantext.clean_texts([None, "hello", None])
    assert result == ["", cleantext.clean("hello"), ""]


def test_clean_texts_generator_input():
    gen = (t for t in ["hello", "world"])
    result = cleantext.clean_texts(gen)
    assert result == [cleantext.clean("hello"), cleantext.clean("world")]


# ---------------------------------------------------------------------------
# exceptions tests
# ---------------------------------------------------------------------------


def test_exception_preserve_hyphenated_word():
    """Core issue #19 use case: keep hyphens in compound words with no_punct."""
    result = cleantext.clean("drive-thru is great", no_punct=True, exceptions=["drive-thru"])
    assert "drive-thru" in result


def test_exception_regex_pattern():
    """Regex pattern preserves multiple compound words."""
    result = cleantext.clean(
        "drive-thru and pick-up and text---cleaning",
        no_punct=True,
        exceptions=[r"\w+-\w+"],
    )
    assert "drive-thru" in result
    assert "pick-up" in result
    # triple dash is not \w+-\w+, so it should be cleaned
    assert "---" not in result


def test_exception_none_default():
    """None exceptions should behave like no exceptions."""
    text = "hello, world!"
    assert cleantext.clean(text, exceptions=None) == cleantext.clean(text)


def test_exception_empty_list():
    """Empty list should behave like no exceptions."""
    text = "hello, world!"
    assert cleantext.clean(text, exceptions=[]) == cleantext.clean(text)


def test_exception_survives_lowercase():
    """Exception text preserved verbatim even when lower=True."""
    result = cleantext.clean("Keep My-Case here", lower=True, no_punct=True, exceptions=["My-Case"])
    assert "My-Case" in result


def test_exception_survives_ascii_conversion():
    """Exception text preserved through to_ascii step."""
    result = cleantext.clean("café-latte is nice", to_ascii=True, no_punct=True, exceptions=["café-latte"])
    assert "café-latte" in result


def test_exception_survives_digit_replacement():
    """Exception text preserved through digit replacement."""
    result = cleantext.clean("version-3.2 is out", no_digits=True, no_punct=True, exceptions=[r"version-3\.2"])
    assert "version-3.2" in result


def test_exception_survives_number_replacement():
    """Exception text preserved through number replacement."""
    result = cleantext.clean("build-42 released", no_numbers=True, no_punct=True, exceptions=[r"build-42"])
    assert "build-42" in result


def test_exception_survives_url_replacement():
    """Exception text preserved through URL replacement."""
    result = cleantext.clean(
        "visit http://keep-me.com today",
        no_urls=True,
        exceptions=[r"http://keep-me\.com"],
    )
    assert "http://keep-me.com" in result


def test_exception_multiple_patterns():
    """Multiple exception patterns each protect their matches."""
    result = cleantext.clean(
        "drive-thru and $100",
        no_punct=True,
        no_currency_symbols=True,
        exceptions=[r"\w+-\w+", r"\$\d+"],
    )
    assert "drive-thru" in result
    assert "$100" in result


def test_exception_multiple_matches_one_pattern():
    """One pattern can match multiple spans."""
    result = cleantext.clean(
        "a-b and c-d and e-f",
        no_punct=True,
        exceptions=[r"\w+-\w+"],
    )
    assert "a-b" in result
    assert "c-d" in result
    assert "e-f" in result


def test_exception_no_match_pattern():
    """A pattern that matches nothing has no effect."""
    text = "hello world"
    assert cleantext.clean(text, exceptions=["zzzzz"]) == cleantext.clean(text)


def test_exception_clean_texts_sequential():
    """clean_texts passes exceptions through (sequential)."""
    texts = ["drive-thru", "pick-up"]
    result = cleantext.clean_texts(texts, n_jobs=1, no_punct=True, exceptions=[r"\w+-\w+"])
    assert "drive-thru" in result[0]
    assert "pick-up" in result[1]


def test_exception_clean_texts_parallel():
    """clean_texts passes exceptions through (parallel)."""
    texts = ["drive-thru", "pick-up", "one-two"]
    result = cleantext.clean_texts(texts, n_jobs=2, no_punct=True, exceptions=[r"\w+-\w+"])
    assert "drive-thru" in result[0]
    assert "pick-up" in result[1]
    assert "one-two" in result[2]


def test_exception_clean_transformer():
    """CleanTransformer passes exceptions through."""
    from cleantext.sklearn import CleanTransformer

    ct = CleanTransformer(no_punct=True, exceptions=[r"\w+-\w+"])
    result = ct.transform(["drive-thru is great"])
    assert "drive-thru" in result[0]


def test_exception_clean_transformer_get_params():
    """CleanTransformer.get_params includes exceptions."""
    from cleantext.sklearn import CleanTransformer

    ct = CleanTransformer(exceptions=[r"\w+-\w+"])
    params = ct.get_params()
    assert params["exceptions"] == [r"\w+-\w+"]


def test_exception_clean_transformer_clone():
    """CleanTransformer can be cloned with exceptions."""
    from sklearn.base import clone
    from cleantext.sklearn import CleanTransformer

    ct = CleanTransformer(no_punct=True, exceptions=[r"\w+-\w+"])
    ct2 = clone(ct)
    result = ct2.transform(["drive-thru is great"])
    assert "drive-thru" in result[0]
