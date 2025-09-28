.PHONY: help setup db-up db-down extract transform test lint docs full-pipeline

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install Python dependencies
	pip install -r requirements.txt
	cd dbt_project && dbt deps

db-up: ## Start PostgreSQL via Docker Compose
	docker-compose up -d postgres
	@echo "Waiting for PostgreSQL to be ready..."
	@sleep 3
	@echo "PostgreSQL is ready."

db-down: ## Stop and remove containers
	docker-compose down -v

db-schema: ## Initialize raw schema in PostgreSQL
	docker-compose exec -T postgres psql -U pipeline -d defi_pipeline -f /docker-entrypoint-initdb.d/init.sql || \
	psql $(DATABASE_URL) -f docker/init.sql

extract: ## Run all Python extractors
	python extract/run_extraction.py

extract-etherscan: ## Run only Etherscan extractor
	python -m extract.run_extraction --source etherscan

extract-defillama: ## Run only DeFiLlama extractor
	python -m extract.run_extraction --source defillama

extract-dune: ## Run only Dune extractor
	python -m extract.run_extraction --source dune

extract-coingecko: ## Run only CoinGecko extractor
	python -m extract.run_extraction --source coingecko

transform: ## Run dbt models + tests
	cd dbt_project && dbt build --profiles-dir .

transform-staging: ## Run only staging layer
	cd dbt_project && dbt build --select staging --profiles-dir .

transform-marts: ## Run only marts layer
	cd dbt_project && dbt build --select marts --profiles-dir .

test: ## Run Python unit tests
	pytest tests/ -v --cov=extract --cov-report=term-missing

lint: ## Lint Python code
	ruff check extract/ tests/

docs: ## Generate & serve dbt docs
	cd dbt_project && dbt docs generate && dbt docs serve

full-pipeline: db-up extract transform ## Run full pipeline end-to-end
	@echo "✅ Full pipeline completed successfully!"
