NAME := models
EPYDOC_PARSE = vigilo\.models\.(tables|test)
all: build
include buildenv/Makefile.common

install: install_python install_data
install_pkg: install_python_pkg install_data

install_python: settings.ini $(PYTHON)
	$(PYTHON) setup.py install --root=$(DESTDIR) --record=INSTALLED_FILES
install_python_pkg: settings.ini $(PYTHON)
	$(PYTHON) setup.py install --single-version-externally-managed --root=$(DESTDIR)

install_data: $(wildcard tools/*)
	mkdir -p $(DESTDIR)$(BINDIR)
	install -p -m 755 tools/* $(DESTDIR)$(BINDIR)

lint: lint_pylint
tests: tests_nose
clean: clean_python

.PHONY: install_pkg install_python install_python_pkg install_data
