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


start:
	./roverlib-wrapper/bin/roverlib-wrapper python3 run.py


test: lint install-deps clean
	. .venv/bin/activate; ./roverlib-wrapper/bin/roverlib-wrapper pytest


install-test:
	. .venv/bin/activate; uv pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade roverlib

install:
	. .venv/bin/activate; uv pip install --upgrade roverlib

upload: build
	. .venv/bin/activate; python3 -m twine upload dist/*
