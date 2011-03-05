NAME := models
EPYDOC_PARSE = vigilo\.models\.(tables|test)
all: build
include buildenv/Makefile.common

install: $(PYTHON)
	$(PYTHON) setup.py install --single-version-externally-managed --root=$(DESTDIR) --record=INSTALLED_FILES
	chmod a+rX -R $(DESTDIR)$(PREFIX)/lib*/python*/*
	mkdir -p $(DESTDIR)$(BINDIR)
	install -p -m 755 tools/* $(DESTDIR)$(BINDIR)

lint: lint_pylint
tests: tests_nose
clean: clean_python
