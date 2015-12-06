#!/bin/bash

branch=${1:-master}

git remote update origin > /dev/null

LOCAL=$(git rev-parse @{0})
REMOTE=$(git rev-parse origin/$branch)

[[ "$LOCAL" == "$REMOTE" ]] && exit 0

git checkout origin/$branch
source env/bin/activate

cd edirtic
[[ -f requirements.local.txt ]] && pip install -r requirements.local.txt --upgrade
pip install -r requirements.txt --upgrade
./manage.py migrate
echo yes | ./manage.py collectstatic
cd ..

touch touch-to-reload
