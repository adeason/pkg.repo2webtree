help:
	@echo "Targets:"
	@echo "  make check: Run tests"

TESTS=test -v
check:
	python3 -m pytest $(TESTS)
