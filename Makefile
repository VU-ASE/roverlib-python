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


# start:
# 	./roverlib-wrapper/bin/roverlib-wrapper python3 run.py


update:
	git submodule update --recursive --remote
	cp -r rovercom/packages/python/gen/* lib/roverlib/src/pb/

	

install-test:
	. .venv/bin/activate; uv pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade roverlib


# The reason we are exporting the path here is so that roverlib can
# call roverlib-wrapper as a native binary, since that will be the case
# on the rover
test: lint install-deps clean
	. .venv/bin/activate; env PATH=$$PATH:./roverlib-wrapper/bin/ python3 test.py

test-producer: lint install-deps clean update
	. .venv/bin/activate; ./roverlib-wrapper/bin/roverlib-wrapper -service-yaml ./lib/service_producer.yaml "python3 lib/test_producer.py"

test-consumer: lint install-deps clean update
	. .venv/bin/activate; ./roverlib-wrapper/bin/roverlib-wrapper -service-yaml ./lib/service_consumer.yaml "python3 lib/test_consumer.py"

install:
	. .venv/bin/activate; uv pip install --upgrade roverlib

upload: build
	. .venv/bin/activate; python3 -m twine upload dist/*
