FROM python:3.9

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable


# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/2.36/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

# Create work dir
# Remove this following later 
# Thats not be necessary
RUN mkdir -p /home/lib/

# Set up work directory
WORKDIR /home/lib

# Set up env variable
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy data dir
RUN mkdir -p data/news/
RUN mkdir -p bot/

# Copy source code
COPY bot/ bot/

# Install dependencies
RUN pip install -r bot/requirements.txt
# Exposing port
EXPOSE 8000
CMD [ "python", "bot/pkg/utils.py", "--scraper=current", "--register_mode=fs" ]

