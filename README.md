# Release Weaver

Turn conventional commit subjects into readable, grouped release notes.

## Features

- Features, fixes, documentation, and maintenance sections
- Scope extraction, breaking-change markers, and duplicate removal
- Optional repository links for commit hashes
- JSON or Markdown output with explicit unparsed subjects

## Get started

Requires **Python 3.11+**. No third-party packages or installation step.

```sh
git clone https://github.com/oexwashere/release-weaver.git
cd release-weaver
python3 app.py --help
```

## Examples

```sh
python3 app.py examples/commits.txt --version v1.0.0 --date 2026-01-01
python3 app.py examples/commits.txt --version v1.0.0 --json
# To use your own history:
git log --format='%h %s' > commits.txt
python3 app.py commits.txt --version v1.1.0 > release-notes.md
```

Example files are intentionally small and contain no real credentials or user data. Output goes to stdout, making it easy to redirect into a report. Errors go to stderr.

## Verify

```sh
python3 -m unittest -v
python3 -m py_compile app.py
```

Tests use temporary directories when filesystem access is needed. They do not modify your working data or require a network connection. GitHub Actions is configured for Python 3.11, 3.12, and 3.13.

## Architecture

`app.py` contains the reusable functions and CLI entry point. `test_app.py` exercises boundary conditions and representative workflows. `examples/` contains runnable fixtures.

Subjects are parsed into type, scope, optional commit hash, breaking marker, and description. Breaking changes get their own section. Unknown formats remain visible under Other changes rather than disappearing. Markdown metacharacters in subjects are escaped.

## Exit codes

`0` means the requested operation completed; `2` means a usage, input, or filesystem failure.

## Limitations and data handling

This parses one-line subjects. It does not inspect commit bodies, recognize `BREAKING CHANGE:` footers, choose versions, create tags, or publish releases. Generated notes are a draft for human review. Optional commit links require a plain HTTPS repository URL.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused and include a regression test when behavior changes.

## License

[MIT](LICENSE) · oexwashere
