# QRSPI — Research

Date: 2026-07-22

## Existing repository facts

- The starter provides a Python CLI, a ten-row fictional CSV, functional and OOP API stubs, starter tests, and documentation scaffolds.
- The existing Trunk configuration enables overlapping Python formatters and linters; the planned quality layer will replace that overlap with a smaller set of checks.
- The local toolchain has uv, Trunk, Graphite, and Python 3.14 available.

## Course and prior-project evidence

- The supplied rubric requires a valid 15–20-song dataset, numeric scoring, sorted recommendations, three profile outputs, a Model Card, and four optional stretch features.
- Project 1 feedback highlighted missing evidence artifacts and incomplete model-comparison documentation.
- Project 2 earned full credit but revealed process risks: inconsistent boundary validation, duplicate test builders, and documentation/status updates that could drift from the implementation layer.

## External-source facts

- MusicBrainz provides a REST API and publishes its core metadata under CC0. It can verify recording identity and release-year provenance without copying audio, lyrics, cover art, or proprietary feature analysis.
- Spotify's November 2024 developer update states that Audio Features and Audio Analysis are unavailable to new Web API applications, so they are not a viable source for this classroom catalog.
