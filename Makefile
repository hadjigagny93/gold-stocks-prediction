image-bot:
	docker build -f ./docker/bot/Dockerfile --tag  bot-selenium:latest . 
container-bot:
	docker run -it bot-selenium:latest /bin/bash

image-api:
	docker build -f ./docker/backend/Dockerfile --tag api-django:latest .
container-api:
	docker run -it api-django:latest /bin/bash

docker run -d --name=me bot-selenium:latest tail -f /dev/null