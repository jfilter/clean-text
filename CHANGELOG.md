# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.1] - 2026-01-28

### Fixed

- Fix scipy version constraints for Python 3.13 compatibility (use scipy 1.14+ for Python 3.10+)
- Fix GitHub Actions badge URL in README
- Fix test imports to skip sklearn tests when extra not installed

### Added

- Add pre-commit hooks for ruff lint and format
- Add RELEASING.md with comprehensive release guide

## [0.7.0] - 2026-01-28

### Added

-   Add `clean_texts()` function for batch cleaning with multiprocessing support ([#20](https://github.com/jfilter/clean-text/issues/20))
-   Add code snippet and file path filters ([#23](https://github.com/jfilter/clean-text/issues/23))
-   Add option to remove IP addresses ([#34](https://github.com/jfilter/clean-text/issues/34))
-   Add language support for Danish, Spanish, Faroese, French, Icelandic, Italian, Norwegian, Scandinavian, and Swedish ([#36](https://github.com/jfilter/clean-text/issues/36))
-   Add regex exceptions to `clean()` ([#19](https://github.com/jfilter/clean-text/issues/19))

### Fixed

-   Fix phone numbers with 00 international prefix ([#10](https://github.com/jfilter/clean-text/issues/10))
-   Fix number replacement regex ([#29](https://github.com/jfilter/clean-text/issues/29), [#27](https://github.com/jfilter/clean-text/issues/27), [#33](https://github.com/jfilter/clean-text/issues/33))

### Changed

-   Improve scikit-learn compatibility for `CleanTransformer` ([#31](https://github.com/jfilter/clean-text/issues/31))
-   Use emoji module's recommended APIs for emoji 2.x
-   Update emoji and pandas dependency constraints ([#37](https://github.com/jfilter/clean-text/issues/37), [#38](https://github.com/jfilter/clean-text/issues/38))
-   Bump scikit-learn minimum to >=1.5.0 (security fix)
-   Modernize project tooling: replace black + pylint with ruff, update CI to Python 3.9–3.13
-   Drop Python 3.6–3.8, require Python >=3.9

## [0.6.0]

### Added

-   Add pipeline for scikit-learn by [sadra-barikbin](https://github.com/sadra-barikbin) ([#21](https://github.com/jfilter/clean-text/issues/21))
-   Add utility function to remove substrings from text

### Changed

-   Drop Python 3.6, support Python 3.10
-   Improve documentation
-   Rename default branch from `master` to `main`

## [0.5.0] - 2021-08-31

### Changed

-   New way to handle unicode to avoid weird changes ([#17](https://github.com/jfilter/clean-text/issues/17))

## [0.4.0] - 2021-04-12

### Fixed

-   Fix emoji & whitespace handling

## [0.3.0] - 2020-10-18

### Changed

-   Various minor improvements

## [0.2.1] - 2019-07-24

### Fixed

-   Minor fixes

## [0.2.0] - 2019-07-24

### Changed

-   Support Python 3.8 and 3.9
-   Various minor improvments

## [0.1.1] - 2019-04-24

### Fixed

-   Minor fixes

## [0.1.0] - 2019-04-24

### Added

-   Initial release
