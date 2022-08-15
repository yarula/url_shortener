clean:
	docker-compose down --remove-orphans
	docker network rm shortener_net || true

clean_api:
	docker-compose stop shortener.api

clean_db:
	docker-compose stop shortener.db

clean_ocpp:
	docker-compose stop shortener.ocpp

network:
	docker network create shortener_net || true

shortener.db: network
	docker-compose up -d shortener.db

shortener.api:
	docker-compose up --build -d shortener.api

up: clean network shortener.db shortener.api

up_api: clean_api shortener.api

up_db: clean_db shortener.db
