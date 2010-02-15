NAME := models
all: build
install:
	$(PYTHON) setup.py install --single-version-externally-managed --root=$(DESTDIR) --record=INSTALLED_FILES

include ../glue/Makefile.common
lint: lint_pylint
tests: tests_nose
clean: clean_python
