GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}
FLAKE8_FLAGS = --ignore=W503,E501

.PHONY: help clean test clean-build lint lint_black lint_isort black isort formatter run_dev migrations migrate makemessages coverage show_urls

.DEFAULT: help

help:
	@echo "make clean:"
	@echo "       Removes all pyc, pyo and __pycache__"
	@echo ""
	@echo "make clean-build:"
	@echo "       Clear all build directories"
	@echo ""
	@echo "make test:"
	@echo "       Run tests with coverage, lint, and clean commands"
	@echo ""


clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . | grep -E "__pycache__|.pytest_cache|.pyc|.DS_Store$$" | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -f *.egg
	@rm -f *.eggs
	@rm -rf *.egg-info/
	@coverage erase || exit 1
	@rm -rf htmlcov/
	@rm -f .coverage
	@rm -f .coverage.*
	@rm -rf .cache/
	@rm -f coverage.xml
	@rm -f *.cover
	@rm -rf testresults
	@rm -rf .pytest_cache/


clean-build: clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

lint:
	@pylint kernel_catalogo_videos/

lint_black:
	@docker run --rm --volume $(pwd):/src --workdir /src pyfound/black:latest_release black --check .

lint_isort:
	@isort --check-only apps/ src/

## @ formatacao
black:
	@docker run --rm --volume $(pwd):/src --workdir /src pyfound/black:latest_release black .

isort:
	@isort kernel_catalogo_videos/

formatter: isort black

coverage:
	@coverage html

test: clean-build
	@pytest
