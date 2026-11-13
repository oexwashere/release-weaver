# Design notes

## Scope

Turn conventional commit subjects into readable, grouped release notes.

## Implementation decisions

Subjects are parsed into type, scope, optional commit hash, breaking marker, and description. Breaking changes get their own section. Unknown formats remain visible under Other changes rather than disappearing. Markdown metacharacters in subjects are escaped.

## Boundaries

This parses one-line subjects. It does not inspect commit bodies, recognize `BREAKING CHANGE:` footers, choose versions, create tags, or publish releases. Generated notes are a draft for human review. Optional commit links require a plain HTTPS repository URL.

## Verification

The Python unittest suite uses deterministic fixtures and temporary directories for filesystem tests.

Tests describe expected behavior rather than depending on a live external service. CI configuration is included, but remote CI execution is not implied by local test results.
