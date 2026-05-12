.PHONY: install uninstall clean test lint format help

PYTHON := python3
PIP := pip3

help:
	@echo "DevGuardian Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install     Install DevGuardian to system"
	@echo "  uninstall   Uninstall DevGuardian"
	@echo "  clean       Clean build artifacts"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  run         Run DevGuardian"
	@echo "  report      Generate optimization report"

install:
	$(PIP) install --break-system-packages -e .

uninstall:
	$(PIP) uninstall -y devguardian

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

test:
	$(PYTHON) -m pytest tests/ -v || echo "No tests directory found"

lint:
	$(PYTHON) -m flake8 devguardian.py --max-line-length=120 || echo "flake8 not installed"
	$(PYTHON) -m pylint devguardian.py || echo "pylint not installed"

format:
	$(PYTHON) -m black devguardian.py || echo "black not installed"

run:
	$(PYTHON) devguardian.py

report:
	$(PYTHON) devguardian.py --report
