.PHONY: lint, install-deps, clean, build, test, install-test, upload-test

lint:
	@echo "Lint check..."
	@ruff check
	@ruff format

install-deps:
	. .venv/bin/activate; uv pip install -r requirements.txt

clean:
	rm -rf dist
	rm -rf build

build: lint install-deps clean
	. .venv/bin/activate; python3 setup.py bdist_wheel sdist


test: lint install-deps clean
	. .venv/bin/activate; pytest


install-test:
	. .venv/bin/activate; uv pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade roverlib

upload-test: build
	. .venv/bin/activate; python3 -m twine upload --repository testpypi dist/*
