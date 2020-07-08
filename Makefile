python := python3
package := $(shell $(python) setup.py --name)
version := $(shell $(python) setup.py --version)
sdist := dist/$(package)-$(version).tar.gz
wheel := dist/$(package)-$(version)-py3-none-any.whl
sources := setup.py $(shell find $(package) -type f -print)
venv := .venv/.dirstate
venv_packages := black coverage mypy pip pyenchant pylint wheel

export PATH := $(CURDIR)/.venv/bin:$(PATH)

.PHONY: 
build: $(sdist) $(wheel)


$(sdist): $(sources)
	$(python) setup.py sdist


$(wheel): $(sources)
	$(python) setup.py bdist_wheel


.PHONY: venv
venv: $(venv)

$(venv): setup.py
	$(python) -m venv .venv
	$(python) -m pip install --upgrade $(venv_packages)
	$(python) -m pip install --upgrade --editable .
	touch $@


.PHONY: test
test: $(venv)
	coverage run --source=$(package) -m unittest discover --verbose --failfast tests
	coverage report


.PHONY: lint
lint: $(venv)
	pylint --rcfile=.pylintrc myresume
	mypy myresume


clean:
	rm -rf .coverage .venv build dist htmlcov
