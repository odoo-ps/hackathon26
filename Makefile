# Trivi'Hackathon 2026: shortcuts around docker compose (macOS / Linux).
# On Windows, use the docker compose commands listed in README.md.

DB := trivia
# every trivia_* module of the repository
MODULES := $(shell find . -mindepth 2 -maxdepth 2 -name __manifest__.py -path './trivia_*' | cut -d/ -f2 | sort | paste -s -d, -)
# one-off container, run while the server is stopped (two Odoo processes initialising
# the same database at the same time collide)
ODOO := docker compose run --rm odoo odoo -d $(DB)

# Odoo Enterprise, pinned on the commit that matches the Odoo image of docker-compose.yml
# (needs a GitHub account that can read odoo/enterprise; without it, Odoo Community is used)
ENTERPRISE_REPO ?= git@github.com:odoo/enterprise.git
ENTERPRISE_REF := c22fa0eff147a5f201899fb4774388343681ddba

.PHONY: help up down enterprise init update shell psql logs reset

help: ## Show this help
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-11s %s\n", $$1, $$2}'

up: ## Start Odoo and PostgreSQL in the background
	docker compose up -d

down: ## Stop the containers (the database is kept)
	docker compose down

# no access to odoo/enterprise: a warning, and Odoo Community is used (an empty ./enterprise is ignored)
enterprise: ## Download Odoo Enterprise into ./enterprise, if your GitHub account can read it
	@if [ "$$(git -C enterprise rev-parse -q --verify HEAD 2>/dev/null)" = "$(ENTERPRISE_REF)" ]; then \
		echo "Odoo Enterprise: already downloaded"; \
	else \
		echo "Odoo Enterprise: downloading (a few hundred MB)..."; \
		{ [ -d enterprise/.git ] || git init -q enterprise; } \
		&& GIT_TERMINAL_PROMPT=0 git -C enterprise fetch --depth 1 $(ENTERPRISE_REPO) $(ENTERPRISE_REF) \
		&& git -C enterprise -c advice.detachedHead=false checkout -q FETCH_HEAD \
		&& echo "Odoo Enterprise: downloaded" \
		|| echo "Odoo Enterprise: no access to $(ENTERPRISE_REPO), Odoo Community is used"; \
	fi

init: enterprise ## Download Enterprise, create the database, install all the trivia_* modules
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
