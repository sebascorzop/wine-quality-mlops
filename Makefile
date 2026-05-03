.PHONY: install train test lint clean help

help:
	@echo "Available commands:"
	@echo "  make install    - Install project dependencies"
	@echo "  make train      - Run the ML pipeline"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run code linting"
	@echo "  make clean      - Clean generated files"
	@echo "  make all        - Run install, lint, test, and train"

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "Dependencies installed successfully!"

train:
	@echo "Running ML pipeline..."
	python src/train.py
	@echo "Training completed!"

test:
	@echo "Running tests..."
	pytest tests/ -v --tb=short
	@echo "Tests completed!"

lint:
	@echo "Running linting..."
	flake8 src/ --max-line-length=100 --exclude=__pycache__
	@echo "Linting completed!"

format:
	@echo "Formatting code with black..."
	black src/ tests/
	@echo "Formatting completed!"

clean:
	@echo "Cleaning generated files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/
	@echo "Cleanup completed!"

all: install lint test train
	@echo "All tasks completed successfully!"
