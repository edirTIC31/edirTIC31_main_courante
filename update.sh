#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <branche>" >&2
    exit 1
fi

branch="$1"

git remote update origin > /dev/null

LOCAL=$(git rev-parse @{0})
REMOTE=$(git rev-parse origin/$branch)

if [ "$LOCAL" == "$REMOTE" ]; then
    exit 0
fi

git checkout origin/$branch
source env/bin/activate

cd edirtic
pip install -r requirements.local.txt --upgrade
pip install -r requirements.txt --upgrade
./manage.py migrate
echo yes | ./manage.py collectstatic
cd ..

touch touch-to-reload
