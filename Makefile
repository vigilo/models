NAME := models
all: build
lint: lint_pylint
tests: tests_runtests
include ../glue/Makefile.common
