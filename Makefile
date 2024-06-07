package := $(shell pdm show --name)
version := $(shell pdm show --version)
sdist := dist/$(package)-$(version).tar.gz
wheel := dist/$(package)-$(version)-py3-none-any.whl
sources := $(shell find $(package) -type f -print)

.PHONY:
build: $(sdist) $(wheel)


$(sdist): $(sources)
	pdm build --no-wheel


$(wheel): $(sources)
	pdm build --no-sdist


.PHONY: test
test:
	pdm sync --dev
	pdm run coverage run --source=$(package) -m unittest discover --verbose --failfast tests
	pdm run coverage report


.PHONY: lint
lint:
	pdm sync --dev
	pdm run pylint --rcfile=.pylintrc myresume
	pdm run mypy myresume


clean:
	rm -rf .coverage build dist htmlcov
