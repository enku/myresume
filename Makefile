package := $(shell pdm show --name)
version := $(shell pdm show --version)
sdist := dist/$(package)-$(version).tar.gz
wheel := dist/$(package)-$(version)-py3-none-any.whl
sources := $(shell find $(package) -type f -print)
tests := $(shell find tests -type f -print)
python_src := $(filter %.py, $(source) $(tests))

.PHONY:
build: $(sdist) $(wheel)


$(sdist): $(sources)
	pdm build --no-wheel


$(wheel): $(sources)
	pdm build --no-sdist


.PHONY: test
test:
	pdm sync --dev
	pdm run coverage run --source=$(package) -mm tests --failfast
	pdm run coverage report


.PHONY: lint
lint:
	pdm sync --dev
	pdm run pylint --rcfile=.pylintrc myresume
	pdm run mypy myresume


.fmt: $(python_src)
	pdm run isort $?
	pdm run black $?
	touch $@


.PHONY: fmt
fmt: .fmt


clean:
	rm -rf .coverage .fmt build dist htmlcov
