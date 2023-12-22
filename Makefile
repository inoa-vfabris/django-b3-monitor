build:
	docker compose -f docker-compose.yml --env-file .env build

up:
	docker compose -f docker-compose.yml --env-file .env up

ps:
	docker compose -f docker-compose.yml --env-file .env ps

down:
	docker compose -f docker-compose.yml --env-file .env down