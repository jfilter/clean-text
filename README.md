# clean-text

Clean your text with `clean-text` to create normalized text representations. For instance, turn this corrupted input:

```txt
A bunch of \\u2018new\\u2019 references, including [Moana](https://en.wikipedia.org/wiki/Moana_%282016_film%29).


»Yóù àré     rïght &lt;3!«
```

into this

```txt
A bunch of 'new' references, including [moana](<URL>).

"you are right <3!"
```

`clean-text` uses [ftfy](https://github.com/LuminosoInsight/python-ftfy), [unidecode](https://github.com/takluyver/Unidecode) and numerous hand-crafted rules, i.e., RegEx.

## Installation

```bash
pip install clean-text[gpl]
```

This will install the GPL-licensed package [unidecode](https://github.com/takluyver/Unidecode). If it is not available, `clean-text` will resort to Python's [unicodedata.normalize](https://docs.python.org/3.7/library/unicodedata.html#unicodedata.normalize) for [transliteration](https://en.wikipedia.org/wiki/Transliteration). Unicode symbols are encoded to their clostest ASCII equivlaent. So `ê` gets turned into `e`. However, you may also disable this feature altogether.

```bash
pip install clean-text
```

## Usage

```python
from cleantext import clean

clean("some input",
    fix_unicode=True, # fix various unicode errors
    to_ascii=True, # transliterate to closest ASCII representation
    lower=True, # lowercase text
    no_line_breaks=False, # fully strip linebreaks
    no_urls=False, # replace all URLs with a special token
    no_emails=False, # replace all email addresses with a special token
    no_phone_numbers=False, # replace all phone numbers with a special token
    no_numbers=False, # replace all numbers with a special token
    no_digits=False, # replace all digits with a special token
    no_currency_symbols=False, # replace all currency symbols with a special token
    no_punct=False, # fully remove punctuation
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    lang="en" # change to 'de' for German special handling
)
```

Carefully choose the arguments that fit your task. The default parameters are listed above. Whitespace is always normalized.

You may also only use specific functions for cleaning. For this, take a look at the [source code](https://github.com/jfilter/clean-text/blob/master/cleantext/clean.py).

## Development

-   install [Pipenv](https://pipenv.readthedocs.io/en/latest/)
-   get the package: `git clone https://github.com/jfilter/clean-text && cd clean-text && pipenv install`
-   run tests: `pipenv run pytest`

## Contributing

If you have a **question**, found a **bug** or want to propose a new **feature**, have a look at the [issues page](https://github.com/jfilter/clean-text/issues).

**Pull requests** are especially welcomed when they fix bugs or improve the code quality.

If you don't like the output of `clean-text`, consider adding a [test](https://github.com/jfilter/clean-text/tree/master/tests) with your specific input and desired output.

## Acknowledgements

Built upon the work by [Burton DeWilde](https://github.com/bdewilde)'s for [Textacy](https://github.com/chartbeat-labs/textacy).

## License

Apache
