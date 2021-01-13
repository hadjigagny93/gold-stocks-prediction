FROM python:3.9
#RUN mkdir -p /usr/src/backend
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up env variable
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Install dependencies 
RUN pip install --upgrade pip
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt

COPY ./backend/ .
