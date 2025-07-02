.PHONY: help migrate migrate-fresh generate-migration run-migration

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

migrate: ## Run all pending migrations
	alembic upgrade head

migrate-fresh: ## Drop all tables and recreate (fresh start)
	python migrate_fresh.py

generate-migration: ## Generate new migration (use MESSAGE="description" to set message)
	python generate_migration.py --message "$(MESSAGE)"

generate-and-run: ## Generate and run migration in one command
	python generate_migration.py --message "$(MESSAGE)" --run

run-migration: ## Run migrations without generating
	python generate_migration.py --run

status: ## Show migration status
	alembic current
	alembic history

rollback: ## Rollback to previous migration
	alembic downgrade -1

rollback-to: ## Rollback to specific revision (use REVISION="revision_id")
	alembic downgrade $(REVISION) 