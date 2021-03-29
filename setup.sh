#!/bin/bash
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
sudo -u postgres psql
# CREATE DATABASE opensourcecooking;
# CREATE USER babe WITH PASSWORD 'a password';
# ALTER ROLE babe SET client_encoding TO 'utf-8';
# ALTER ROLE babe SET default_transaction_isolation TO 'read committed';
# ALTER ROLE babe SET timezone TO 'UTC';
# GRANT ALL PRIVILEGES ON DATABASE opensourcecooking TO babe;
# \q

