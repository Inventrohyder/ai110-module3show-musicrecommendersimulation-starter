# Changelog

All notable changes to VibeFinder are documented here. This project follows a small, stacked delivery workflow rather than release tags.

## Unreleased

- Established the QRSPI delivery record, ADR process, and GitHub Project workflow.
- Made uv and its lockfile the authoritative Python environment, with pip fallback exports.
- Constrained pytest to the compatible 8.x line to keep the pytest-bdd suite warning-free.
- Reduced Trunk quality checks to a focused, non-overlapping set.
- Configured Bandit to allow pytest assertions while retaining production-code security checks.
- Added locked-environment tests and Trunk quality checks for pull requests and `main`.
