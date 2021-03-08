#!/bin/bash
exec gunicorn --config guni_config.py app.wsgi:app