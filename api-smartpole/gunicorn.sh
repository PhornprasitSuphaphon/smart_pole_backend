#!/bin/sh
gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:4500 --graceful-timeout 30 --timeout 120