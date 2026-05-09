# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-05-09

### Added
- **Stability:** Added configurable `request_timeout` (default 30s) to all providers to prevent hanging.
- **Stability:** Robust JSON decode error handling for API responses with diagnostic info in debug mode.
- **Security:** Restricted filesystem permissions for configuration (700 for directory, 600 for `config.json`).
- **Documentation:** Created `CHANGELOG.md` to track project evolution.

### Changed
- **Architecture:** Refactored CLI to use `argparse` for robust argument parsing and automatic help generation.
- **Architecture:** Implemented a lazy-loading provider registry in `termai/api.py` for better performance and extensibility.
- **Security:** Moved Gemini API key from URL query parameters to secure HTTP headers (`x-goog-api-key`).
- **Codebase:** Refactored providers to extend `BaseProvider` with shared helper methods for DRYer code.
- **Testing:** Overhauled and expanded the test suite to verify security, stability, and architectural changes.
- **Documentation:** Updated `README.md` and `GEMINI.md` to reflect new architecture and security best practices.

## [0.3.3] - 2024-xx-xx (Previous Version)
- Baseline version with basic Gemini and OpenAI support.
- Initial manual CLI parsing logic.
- Basic configuration system.
