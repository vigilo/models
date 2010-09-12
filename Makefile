NAME := models
EPYDOC_PARSE = vigilo\.models\.tables
all: build
include buildenv/Makefile.common

install: $(PYTHON)
	$(PYTHON) setup.py install --single-version-externally-managed --root=$(DESTDIR) --record=INSTALLED_FILES
	mkdir -p $(DESTDIR)$(BINDIR)
	install -p -m 755 tools/* $(DESTDIR)$(BINDIR)

lint: lint_pylint
tests: tests_nose
clean: clean_python
