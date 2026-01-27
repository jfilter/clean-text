try:
    import pandas as pd
    import pytest

    from cleantext.sklearn import CleanTransformer

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

    def test_get_feature_names_out():
        feature_names = transformer.get_feature_names_out()
        assert feature_names == ["Clean Text"]

    def test_fit():
        transformer.fit(["sample1", "sample2"], [0, 1])
        transformer.partial_fit(["sample1", "sample2"])
except ImportError:
    pass
