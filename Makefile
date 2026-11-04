# Trivi'Hackathon 2026: shortcuts around docker compose (macOS / Linux).
# On Windows, use the docker compose commands listed in README.md.

DB := trivia
# every trivia_* module of the repository
MODULES := $(shell find . -mindepth 2 -maxdepth 2 -name __manifest__.py -path './trivia_*' | cut -d/ -f2 | sort | paste -s -d, -)
# one-off container, run while the server is stopped (two Odoo processes initialising
# the same database at the same time collide)
ODOO := docker compose run --rm odoo odoo -d $(DB)

.PHONY: help up down init update shell psql logs reset

help: ## Show this help
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-8s %s\n", $$1, $$2}'

up: ## Start Odoo and PostgreSQL in the background
	docker compose up -d

down: ## Stop the containers (the database is kept)
	docker compose down

init: ## Create the database and install all the trivia_* modules
	docker compose stop odoo
	$(ODOO) -i $(or $(MODULES),base) --stop-after-init
	docker compose up -d

# all the modules: nobody updates the wrong one
update: ## Update all the trivia_* modules and restart Odoo
	docker compose stop odoo
	$(ODOO) -u $(or $(m),$(MODULES),base) --stop-after-init
	docker compose up -d

shell: ## Open an Odoo shell on the database
	docker compose exec odoo odoo shell -d $(DB)

psql: ## Open a PostgreSQL console on the database
	docker compose exec db psql -U odoo $(DB)

logs: ## Follow the logs of Odoo
	docker compose logs -f odoo

reset: ## Delete the containers AND the local database, to start over
	docker compose down -v
