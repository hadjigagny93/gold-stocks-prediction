image:
	echo "build etl docker image for scraping data"
	echo "start build image ..."
	docker build -f ./docker/dockerfile-etl --tag etl:scraper .
	echo "image was sucessfully built..."
container:
	docker run -it etl:scraper /bin/bash
	
