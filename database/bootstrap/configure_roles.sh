#!/usr/bin/env sh
set -eu

export PGPASSWORD="$(cat /run/secrets/postgres_password)"
app_password="$(cat /run/secrets/postgres_app_password)"
migrator_password="$(cat /run/secrets/postgres_migrator_password)"

psql \
  --host postgres \
  --username vittavaan \
  --dbname vittavaan \
  --set app_password="$app_password" \
  --set migrator_password="$migrator_password" \
  --file /bootstrap/configure_roles.sql

unset PGPASSWORD app_password migrator_password
