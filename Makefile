.PHONY: build up down test

IMAGE := tictactoe

build:
	docker build -t $(IMAGE) .

up:
	docker run --rm -p 38000:8000 $(IMAGE)

down:
	docker stop $$(docker ps -q --filter ancestor=$(IMAGE)) 2>/dev/null || true

test:
	docker run --rm $(IMAGE) pytest -v
