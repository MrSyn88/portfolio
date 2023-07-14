#!/bin/zsh

tmux kill-server
cd portfolio
git fetch && git reset origin/main --hard
# read -p "MySQL Host: " MYSQL_HOST
# read -p "MySQL User: " MYSQL_USER
# read -s -p "MySQL Password: " MYSQL_PASSWORD
# read -p "MySQL Database: " MYSQL_DATABASE
# echo "Writing .env file..."
# echo "URL=localhost:5000" > .env
# echo "MYSQL_HOST=$MYSQL_HOST" >> .env
# echo "MYSQL_USER=$MYSQL_USER" >> .env
# echo "MYSQL_PASSWORD=$MYSQL_PASSWORD" >> .env
# echo "MYSQL_DATABASE=$MYSQL_DATABASE" >> .env
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -d -s prod 'cd ~/portfolio;source python3-virtualenv/bin/activate;flask run --host=0.0.0.0'
