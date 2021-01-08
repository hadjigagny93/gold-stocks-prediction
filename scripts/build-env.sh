
# Make sure this script is only run on Linux
value="$(uname)"
if [ "$value" = "Linux" ]
then
  echo "Initializing Requirements Setup..."
else
  echo "Not on a Linux machine. Exiting..."
  exit
fi

# Go home
cd ~

# Configure apt-get resources
sudo sh -c "echo \"deb http://packages.linuxmint.com debian import\" >> /etc/apt/sources.list"
sudo sh -c "echo \"deb http://downloads.sourceforge.net/project/ubuntuzilla/mozilla/apt all main\" >> /etc/apt/sources.list"

# Update aptitude
sudo apt-get update

# Install core dependencies
sudo apt-get install -y --force-yes unzip
sudo apt-get install -y --force-yes xserver-xorg-core
sudo apt-get install -y --force-yes x11-xkb-utils


# Install Xvfb (headless display system)
sudo apt-get install -y --force-yes xvfb

# Install fonts for web browsers
sudo apt-get install -y --force-yes xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic

# Install git
sudo apt-get install git

# Download pyenv for oythone nv management
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# Export env variable to .bashrc file
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"

# in mac os env with zsh shell
#echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
#echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
#echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
#exec "$SHELL"

# Install the required Python build dependencies:
sudo apt-get update; sudo apt-get install -y make build-essential chrpath libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
sudo apt-get install -y --force-yes libxft-dev
sudo apt-get install -y --force-yes libfreetype6 libfreetype6-dev
sudo apt-get install -y --force-yes libfontconfig1 libfontconfig1-dev
sudo apt-get install -y --force-yes python-dev

# Install python 3.9.0
pyenv install 3.9.0

# Set python system to 3.9.0
pyenv global 3.9.0


# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get -f install -y --force-yes
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Install Chromedriver
wget -N http://chromedriver.storage.googleapis.com/2.36/chromedriver_linux64.zip
unzip -o chromedriver_linux64.zip
chmod +x chromedriver
sudo rm -f /usr/local/share/chromedriver
sudo rm -f /usr/local/bin/chromedriver
sudo rm -f /usr/bin/chromedriver
sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

#============
# GeckoDriver
#============
GECKODRIVER_VERSION=latest
GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo $(wget -qO- "https://api.github.com/repos/mozilla/geckodriver/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([0-9.]+)".*/\1/'); else echo $GECKODRIVER_VERSION; fi)
echo "Using GeckoDriver version: "$GK_VERSION
wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz
sudo rm -rf /opt/geckodriver
sudo tar -C /opt -zxf /tmp/geckodriver.tar.gz
rm /tmp/geckodriver.tar.gz
sudo mv /opt/geckodriver /opt/geckodriver-$GK_VERSION
sudo chmod 755 /opt/geckodriver-$GK_VERSION
sudo ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

# Finalize apt-get dependancies
sudo apt-get -f install -y --force-yes

# clone the repo
git clone https://github.com/QaniLabs/gold-stock.git

cd gold-stock

# upgrade pip
pip install --upgrade pip

# Install pipenv
pip install pipenv

# Init and create pipenv virtualenv
pipenv shell

# install all non-dev dependencies in prod env
# but with psycopg2 ... waive it and install psycopg2-binary instead
pipenv install psycopg2-binary

# rm pkgs
rm -r chromedriver_linux64.zip google-chrome-stable_current_amd64.deb
