FROM python:3.9
WORKDIR /usr/src/engine
COPY engine/ .
RUN pip install -r requirements.txt
RUN pip install .
EXPOSE 5000
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "entrypoint.sh"]
