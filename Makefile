image-bot:
	docker build -f ./docker/bot/Dockerfile --tag  bot-selenium:latest . 
container-bot:
	#docker run -it --mount source=my_vol,destination=/home/lib/data bot-selenium:latest python bot/pkg/utils.py --scraper current --register_mode fs
	docker run -it bot-selenium:latest python bot/pkg/utils.py --scraper current --register_mode api

image-api:
	docker build -f ./docker/backend/Dockerfile --tag api-django:latest .
container-api:
	docker run -it api-django:latest /bin/bash

image-engine:
	docker build -f ./docker/engine/Dockerfile --tag engine:latest .
container-api:
	docker run -it -p 5000:5000 engine:latest /bin/bash

#docker run -d --name=me bot-selenium:latest tail -f /dev/null

# svlh -> see volumes on local host (and not try to find them on docker native VM)
svlh:
	docker run -it --privileged --pid=host debian nsenter -t 1 -m -u -n -i ls /var/lib/docker/volumes/my_vol/_data/news

# remove all running containers 
rarc:
	docker container rm $(docker ps -a -q)
#docker run -it -p 8000:8000 bot-selenium:latest python bot/pkg/utils.py --scraper current --register_mode api

postgresrm:
	rm /usr/local/var/postgres/postmaster.pid

docker run -it bot-selenium:latest /bin/bash bot/pkg/test-net.sh