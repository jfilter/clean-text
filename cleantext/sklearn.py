"""
Pipeline transformer for scikit-learn to clean text
"""

from typing import Any, List, Union

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from .clean import clean


class CleanTransformer(TransformerMixin, BaseEstimator):
    """
    Scikit-learn equivalent of :term:`clean` function.
    """

    def __init__(
        self,
        fix_unicode=True,
        to_ascii=True,
        lower=True,
        normalize_whitespace=True,
        no_line_breaks=False,
        strip_lines=True,
        keep_two_line_breaks=False,
        no_urls=False,
        no_emails=False,
        no_phone_numbers=False,
        no_numbers=False,
        no_digits=False,
        no_currency_symbols=False,
        no_punct=False,
        no_emoji=False,
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
        replace_with_punct="",
        lang="en",
    ):
        """
        All parameters are same as the :term:`clean` function.
        """
        self.fix_unicode = fix_unicode
        self.to_ascii = to_ascii
        self.lower = lower
        self.normalize_whitespace = normalize_whitespace
        self.no_line_breaks = no_line_breaks
        self.strip_lines = strip_lines
        self.keep_two_line_breaks = keep_two_line_breaks
        self.no_urls = no_urls
        self.no_emails = no_emails
        self.no_phone_numbers = no_phone_numbers
        self.no_numbers = no_numbers
        self.no_digits = no_digits
        self.no_currency_symbols = no_currency_symbols
        self.no_punct = no_punct
        self.no_emoji = no_emoji
        self.replace_with_url = replace_with_url
        self.replace_with_email = replace_with_email
        self.replace_with_phone_number = replace_with_phone_number
        self.replace_with_number = replace_with_number
        self.replace_with_digit = replace_with_digit
        self.replace_with_currency_symbol = replace_with_currency_symbol
        self.replace_with_punct = replace_with_punct
        self.lang = lang

    def fit(self, X: Any):
        """
        This method is defined for compatibility. It does nothing.
        """
        return self

    def transform(self, X: Union[List[str], pd.Series]) -> Union[List[str], pd.Series]:
        """
        Normalize various aspects of each item in raw text array-like.
        Args:
            X (array-like): an array-like of strings. It could be a list or a Pandas Series.
        Returns:
            array-like[str]: an array-like with the same type as ``X``
                             and with the processed items of ``X`` as content.
        """
        if not (isinstance(X, list) or isinstance(X, pd.Series)):
            raise ValueError("The input must be a list or pd.Series")
        if isinstance(X, pd.Series):
            return X.apply(lambda text: clean(text, **self.get_params()))
        else:
            return list(map(lambda text: clean(text, **self.get_params()), X))
