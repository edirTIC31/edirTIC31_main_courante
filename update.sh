#!/bin/bash

git remote update > /dev/null

LOCAL=$(git rev-parse @{0})
REMOTE=$(git rev-parse origin/$br)

if [ "$LOCAL" == "$REMOTE" ]; then
    continue
fi

git checkout origin/$br
source env/bin/activate

cd edirtic
pip install -r requirements.local.txt --upgrade
pip install -r requirements.txt --upgrade
./manage.py migrate
echo yes | ./manage.py collectstatic
cd ..

touch touch-to-reload
