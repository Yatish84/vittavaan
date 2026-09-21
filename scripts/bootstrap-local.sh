#!/usr/bin/env sh
set -eu

secret_dir="runtime/secrets"
umask 077
mkdir -p "$secret_dir"

if [ ! -s "$secret_dir/postgres_password" ]; then
  printf '%s' 'local-postgres-only' > "$secret_dir/postgres_password"
fi
if [ ! -s "$secret_dir/postgres_app_password" ]; then
  printf '%s' 'local-app-role-only' > "$secret_dir/postgres_app_password"
fi
if [ ! -s "$secret_dir/postgres_migrator_password" ]; then
  printf '%s' 'local-migrator-role-only' > "$secret_dir/postgres_migrator_password"
fi
app_password="$(cat "$secret_dir/postgres_app_password")"
migrator_password="$(cat "$secret_dir/postgres_migrator_password")"
printf 'postgresql+asyncpg://vittavaan_app:%s@postgres:5432/vittavaan' "$app_password" > "$secret_dir/database_url"
printf 'postgresql+asyncpg://vittavaan_migrator:%s@postgres:5432/vittavaan' "$migrator_password" > "$secret_dir/migration_database_url"
unset app_password migrator_password
if [ ! -s "$secret_dir/redis_url" ]; then
  printf '%s' 'redis://:local-valkey-only@valkey:6379/0' > "$secret_dir/redis_url"
fi
if [ ! -s "$secret_dir/object_store_access_key" ]; then
  printf '%s' 'vittavaan-local-access' > "$secret_dir/object_store_access_key"
fi
if [ ! -s "$secret_dir/object_store_secret_key" ]; then
  printf '%s' 'local-object-secret-not-for-shared-use' > "$secret_dir/object_store_secret_key"
fi

printf '%s\n' 'Local-only secret files are ready under runtime/secrets.'
