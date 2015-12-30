#!/bin/bash

branch=${1:-master}

git remote update origin > /dev/null

LOCAL=$(git rev-parse @{0})
REMOTE=$(git rev-parse origin/$branch)

[[ "$LOCAL" == "$REMOTE" ]] && exit 0

git checkout origin/$branch
git submodule update
if [[ ! -d venv ]]; then
    virtualenv venv
fi
source venv/bin/activate

cd django
[[ -f requirements.local.txt ]] && pip install -r requirements.local.txt --upgrade
pip install -r requirements.txt --upgrade
./manage.py migrate
echo yes | ./manage.py collectstatic
cd ..

touch touch-to-reload
