NAME := models
all: build
include ../glue/Makefile.common
lint: lint_pylint
tests: tests_nose
clean: clean_python
