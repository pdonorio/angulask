# Angulask

A project to template flask web server to meet angularjs

## Getting started

```bash
# Clone
git clone https://github.com/pdonorio/angulask.git
# Launch
cd angulask/containers
docker-compose up -d flask
# Debug
docker exec -it containers_flask_1 bash
python3 app.py
```

Then go visit http://localhost to access the web page

## Configuration and defaults

To use your personal directory of JSON files configuration
go edit PATH inside `config/__init__.py`, e.g.

```python
PATH = 'MYCONFIGURATION'
```

Config is located in `config/MYCONFIGURATION`.

Default account:

* Username: 'prototype'
* Password: 'test'