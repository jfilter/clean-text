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
]


def test_replace_phone_numbers():
    for x in phone_numbers:
        x_phone = cleantext.replace_phone_numbers(x, "*PHONE*")
        assert "PHONE" in x_phone and not any(map(str.isdigit, x_phone)), (
            x + " / " + x_phone
        )


def test_replace_numbers():
    text = "I owe $1,000.99 to 123 people for 2 +1 reasons."
    proc_text = "I owe $*NUM* to *NUM* people for *NUM* *NUM* reasons."
    assert cleantext.replace_numbers(text, "*NUM*") == proc_text


def test_remove_punct():
    text = "I can't. No, I won't! It's a matter of \"principle\"; of -- what's the word? -- conscience."
    proc_text = (
        "I cant No I wont Its a matter of principle of  whats the word  conscience"
    )
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
        assert (
            cleantext.replace_currency_symbols(text, replace_with="*CUR* ")
            == proc_text2
        )


def test_fix_bad_unicode():
    text = "and install a \\u2018new\\u2019 society in their"  # and install a ‘new’ society in their
    assert cleantext.fix_bad_unicode(text) == "and install a 'new' society in their"

    assert "všetko" == cleantext.fix_bad_unicode("všetko")
    assert "Všetko" == cleantext.fix_bad_unicode("Všetko")


def test_zero_digits():
    text = "in the 1970s there was 12.3 and 111 11 33 $23 03 wins"
    assert (
        cleantext.replace_digits(text)
        == "in the 0000s there was 00.0 and 000 00 00 $00 00 wins"
    )

    text = "7 Golf Records More 'Unbreakable' Than the Warriors' 73 Wins"
    assert (
        cleantext.replace_digits(text)
        == "0 Golf Records More 'Unbreakable' Than the Warriors' 00 Wins"
    )


def test_to_ascii():
    assert cleantext.to_ascii_unicode("whatëver") == "whatever"
    assert cleantext.to_ascii_unicode("Äpfel»", lang="de") == 'Äpfel"'
    assert cleantext.to_ascii_unicode("Äpfel»", lang="DE") == 'Äpfel"'


def test_whitespace():
    assert cleantext.clean(" peter", normalize_whitespace=False) == " peter"
    assert cleantext.clean(" peter", normalize_whitespace=True) == "peter"
    assert (
        cleantext.clean(" pet\n\ner", normalize_whitespace=True, no_line_breaks=True)
        == "pet er"
    )
    assert (
        cleantext.clean(" pet\n\ner", normalize_whitespace=True, no_line_breaks=False)
        == "pet\ner"
    )


emoji_line = (
    "🤔 🙈 me, se 😌 ds 💕👭👙 hello 👩🏾‍🎓 emoji hello 👨‍👩‍👦‍👦 how are 😊 you today🙅🏽🙅🏽"
)


def test_keep_emojis():
    assert cleantext.clean(emoji_line) == emoji_line


def test_remove_emojis():
    assert (
        cleantext.clean(emoji_line, no_emoji=True)
        == "me, se ds hello emoji hello how are you today"
    )


def test_remove_emojis_no_ascii():
    assert (
        cleantext.clean("😊 you today🙅🏽🙅🏽", to_ascii=False, no_emoji=True) == "you today"
    )


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


def test_remove_trail_leading_whitespace():
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
