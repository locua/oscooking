# opensource cooking website

- Simple and bloat free site for sharing cooking recipes

## Transferring between sqlite db and postgres
  ./manage.py dumpdata --indent 4 > dump.json
  ./manage.py migrate
  ./manage.py loaddata dump.json
