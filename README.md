# `clean-text` [![Build Status](https://img.shields.io/github/workflow/status/jfilter/clean-text/Test)](https://github.com/jfilter/clean-text/actions/workflows/test.yml) [![PyPI](https://img.shields.io/pypi/v/clean-text.svg)](https://pypi.org/project/clean-text/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clean-text.svg)](https://pypi.org/project/clean-text/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/clean-text)](https://pypistats.org/packages/clean-text)

User-generated content on the Web and in social media is often dirty. Preprocess your scraped data with `clean-text` to create a normalized text representation. For instance, turn this corrupted input:

```txt
A bunch of \\u2018new\\u2019 references, including [Moana](https://en.wikipedia.org/wiki/Moana_%282016_film%29).


»Yóù àré     rïght &lt;3!«
```

into this clean output:

```txt
A bunch of 'new' references, including [moana](<URL>).

"you are right <3!"
```

`clean-text` uses [ftfy](https://github.com/LuminosoInsight/python-ftfy), [unidecode](https://github.com/takluyver/Unidecode) and numerous hand-crafted rules, i.e., RegEx.

## Installation

To install the GPL-licensed package [unidecode](https://github.com/takluyver/Unidecode) alongside:

```bash
pip install clean-text[gpl]
```

You may want to abstain from GPL:

```bash
pip install clean-text
```

NB: This package is named `clean-text` and not `cleantext`.

If [unidecode](https://github.com/takluyver/Unidecode) is not available, `clean-text` will resort to Python's [unicodedata.normalize](https://docs.python.org/3.7/library/unicodedata.html#unicodedata.normalize) for [transliteration](https://en.wikipedia.org/wiki/Transliteration).
Transliteration to closest ASCII symbols involes manually mappings, i.e., `ê` to `e`.
`unidecode`'s mapping is superiour but unicodedata's are sufficent.
However, you may want to disable this feature altogether depending on your data and use case.

To make it clear: There are **inconsistencies** between processing text with or without `unidecode`.

## Usage

```python
from cleantext import clean

clean("some input",
    fix_unicode=True,               # fix various unicode errors
    to_ascii=True,                  # transliterate to closest ASCII representation
    lower=True,                     # lowercase text
    no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
    no_urls=False,                  # replace all URLs with a special token
    no_emails=False,                # replace all email addresses with a special token
    no_phone_numbers=False,         # replace all phone numbers with a special token
    no_numbers=False,               # replace all numbers with a special token
    no_digits=False,                # replace all digits with a special token
    no_currency_symbols=False,      # replace all currency symbols with a special token
    no_punct=False,                 # remove punctuations
    replace_with_punct="",          # instead of removing punctuations you may replace them
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    lang="en"                       # set to 'de' for German special handling
)
```

Carefully choose the arguments that fit your task. The default parameters are listed above.

You may also only use specific functions for cleaning. For this, take a look at the [source code](https://github.com/jfilter/clean-text/blob/master/cleantext/clean.py).

So far, only English and German are fully supported. It should work for the majority of western languages. If you need some special handling for your language, feel free to contribute. 🙃

## Development

[Install and use poetry](https://python-poetry.org/).

## Contributing

If you have a **question**, found a **bug** or want to propose a new **feature**, have a look at the [issues page](https://github.com/jfilter/clean-text/issues).

**Pull requests** are especially welcomed when they fix bugs or improve the code quality.

If you don't like the output of `clean-text`, consider adding a [test](https://github.com/jfilter/clean-text/tree/master/tests) with your specific input and desired output.

## Related Work

-   https://github.com/pudo/normality
-   https://github.com/davidmogar/cucco
-   https://github.com/lyeoni/prenlp
-   https://github.com/chartbeat-labs/textacy
-   https://github.com/jbesomi/texthero
-   https://github.com/s/preprocessor
-   https://github.com/facebookresearch/cc_net
-   https://github.com/cbaziotis/ekphrasis
-   https://github.com/artefactory/NLPretext

## Acknowledgements

Built upon the work by [Burton DeWilde](https://github.com/bdewilde) for [Textacy](https://github.com/chartbeat-labs/textacy).

## License

Apache

## Sponsoring

This work was created as part of a [project](https://github.com/jfilter/ptf-kommentare) that was funded by the German [Federal Ministry of Education and Research](https://www.bmbf.de/en/index.html).

<img src="./bmbf_funded.svg">
