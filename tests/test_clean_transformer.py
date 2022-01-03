import cleantext
import pandas as pd

transformer = cleantext.CleanTransformer()

def test_not_list_or_series():
    transformer.transform('sample text')

def test_not_list_of_string():
    transformer.transform([1,2,3])

def test_not_series_of_string():
    transformer.transform(pd.Series([1,2,3]))

def test_len_output_and_input():
    assert len(transformer.transform(['sample1','sample2','sample3'])) == 3

def test_set_params():
    transformer.set_params(no_line_breaks=True, no_digits=True)
    assert transformer.get_params()['no_line_breaks']
    assert transformer.get_params()['no_digits']
