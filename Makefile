.DEFAULT_GOAL := help

# Display available targets when invoked without a target.
.PHONY: help quality build publish
help:
	@printf "Available targets:\n"
	@printf "  quality  Run formatting, linting, and tests.\n"
	@printf "  build    Build source and wheel distributions.\n"
	@printf "  publish  Build and publish distributions to PyPI.\n"

quality:
	poetry run pre-commit run --all-files --show-diff-on-failure
	poetry run pytest

build:
	poetry build

publish: build
	poetry publish
