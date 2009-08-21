NAME = models
BUILDENV = ../glue
PYTHON = $(BUILDENV)/bin/python

all: $(PYTHON)
	$(PYTHON) setup.py build

$(PYTHON):
	make -C $(BUILDENV) bin/python

clean:
	find $(CURDIR) \( -name "*.pyc" -o -name "*~" \) -delete

buildclean: clean
	rm -rf eggs develop-eggs parts .installed.cfg bin

apidoc: doc/apidoc/index.html
doc/apidoc/index.html: src/vigilo/$(NAME)
	rm -rf $(CURDIR)/doc/apidoc/*
	PYTHONPATH=$(BUILDENV):src $(PYTHON) "$$(which epydoc)" -o $(dir $@) -v \
		   --name Vigilo --url http://www.projet-vigilo.org \
		   --docformat=epytext vigilo.$(NAME)

lint: $(PYTHON) src/vigilo/$(NAME)
	-PYTHONPATH=src $(PYTHON) $$(which pylint) src/vigilo/$(NAME)


.PHONY: all clean buildclean apidoc lint tests

