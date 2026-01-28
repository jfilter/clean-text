# Releasing

This document describes how to release a new version of `clean-text`.

## Prerequisites

- Push access to the repository
- PyPI account with upload permissions for `clean-text`
- PyPI API token configured: `poetry config pypi-token.pypi <your-token>`

## Release Checklist

### 1. Ensure CI is green

```bash
gh run list --limit 5
```

All tests must pass on main before releasing.

### 2. Update version numbers

Update the version in both files:

- `pyproject.toml` — `version = "X.Y.Z"`
- `cleantext/__init__.py` — `__version__ = "X.Y.Z"`

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (X): Breaking changes
- **MINOR** (Y): New features, backward compatible
- **PATCH** (Z): Bug fixes, backward compatible

### 3. Update CHANGELOG.md

Move entries from `[Unreleased]` to a new version section with today's date:

```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

### 4. Commit and tag

```bash
git add pyproject.toml cleantext/__init__.py CHANGELOG.md
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

### 5. Create GitHub Release

Create a release on GitHub with release notes:

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file - <<'EOF'
## What's Changed

### Added
- Feature 1
- Feature 2

### Fixed
- Bug fix 1

**Full Changelog**: https://github.com/jfilter/clean-text/compare/vPREVIOUS...vX.Y.Z
EOF
```

Or create interactively:

```bash
gh release create vX.Y.Z --generate-notes
```

### 6. Build and publish to PyPI

```bash
poetry build
poetry publish
```

Verify the release:
- https://pypi.org/project/clean-text/

### 7. Verify installation

```bash
pip install --upgrade clean-text
python -c "import cleantext; print(cleantext.__version__)"
```

## Quick Release Script

For convenience, here's the full release flow (replace `X.Y.Z` with the actual version):

```bash
VERSION="X.Y.Z"

# Verify CI is green
gh run list --limit 3

# Update versions (do this manually in your editor)
# - pyproject.toml
# - cleantext/__init__.py
# - CHANGELOG.md

# Commit, tag, push
git add pyproject.toml cleantext/__init__.py CHANGELOG.md
git commit -m "Release v${VERSION}"
git tag "v${VERSION}"
git push origin main --tags

# Create GitHub release
gh release create "v${VERSION}" --generate-notes

# Build and publish
poetry build
poetry publish

# Verify
pip install --upgrade clean-text
python -c "import cleantext; print(cleantext.__version__)"
```

## Troubleshooting

### PyPI authentication error

```bash
# Set your API token
poetry config pypi-token.pypi pypi-XXXXXXXXXXXX

# Or use environment variable
export POETRY_PYPI_TOKEN_PYPI=pypi-XXXXXXXXXXXX
poetry publish
```

### Tag already exists

If you need to re-tag (e.g., forgot to include a fix):

```bash
# Delete local and remote tag
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z

# Re-tag after fixing
git tag vX.Y.Z
git push origin --tags
```

### Failed publish, need to retry

PyPI doesn't allow re-uploading the same version. If the upload partially failed, contact PyPI support or bump to a patch version (e.g., `0.7.0` → `0.7.1`).
