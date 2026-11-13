# Contributing to Release Weaver

Describe the problem, expected behavior, and a minimal example in an issue or pull request. Keep unrelated changes separate.

Before submitting, run:

```sh
python3 -m unittest -v
```

Add regression coverage for calculations, parsing, or state transitions. UI changes should be checked with keyboard input and a narrow screen. Do not add external services, analytics, or hidden data transmission. Keep examples synthetic and never include credentials or private datasets.

Preserve standard-library-only operation.
