#!/bin/bash
echo "BUILD START"
python3 -m pip install -r requirements.txt
python3 NihongoDekita/manage.py collectstatic --noinput --clear
mv staticfiles public/static
echo "BUILD END"