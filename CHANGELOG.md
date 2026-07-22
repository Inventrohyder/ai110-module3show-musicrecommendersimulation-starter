# Changelog

All notable changes to VibeFinder are documented here. This project follows a small, stacked delivery workflow rather than release tags.

## Unreleased

- Established the QRSPI delivery record, ADR process, and GitHub Project workflow.
- Made uv and its lockfile the authoritative Python environment, with pip fallback exports.
- Constrained pytest to the compatible 8.x line to keep the pytest-bdd suite warning-free.
- Reduced Trunk quality checks to a focused, non-overlapping set.
- Configured Bandit to allow pytest assertions while retaining production-code security checks.
- Added locked-environment tests and Trunk quality checks for pull requests and `main`.
- Kept markdownlint but disabled MD013 so captured CLI tables and source URLs remain exact.
- Preserved the starter catalog, extended it with ten verified recordings, and added the explainable core scorer.
- Added a portable, explainable command-line recommendation flow.
- Added three profile evaluations, BDD scenarios, and a controlled energy-feature experiment.
- Audited all required-rubric evidence before starting stretch work.
