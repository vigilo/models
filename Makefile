NAME := models
all: build
lint: lint_pylint
tests: tests_nose
include ../glue/Makefile.common
