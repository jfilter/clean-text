try:
    from cleantext.sklearn import CleanTransformer
    import pandas as pd

    import pytest

    transformer = CleanTransformer()

    def test_not_list_or_series():
        with pytest.raises(ValueError):
            transformer.transform("sample text")

    def test_not_list_of_string():
        assert transformer.transform([1, 2, 3]) == ["1", "2", "3"]

    def test_not_series_of_string():
        result = transformer.transform(pd.Series([1, 2, 3]))
        assert result.tolist() == ["1", "2", "3"]

    def test_len_output_and_input():
        assert len(transformer.transform(["sample1", "sample2", "sample3"])) == 3

    def test_set_params():
        transformer.set_params(no_line_breaks=True, no_digits=True)
        assert transformer.get_params()["no_line_breaks"]
        assert transformer.get_params()["no_digits"]

except ImportError:
    pass
