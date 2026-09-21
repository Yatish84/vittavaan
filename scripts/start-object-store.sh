#!/bin/sh
set -eu

export RUSTFS_ACCESS_KEY="$(cat /run/secrets/object_store_access_key)"
export RUSTFS_SECRET_KEY="$(cat /run/secrets/object_store_secret_key)"
export RUSTFS_ADDRESS="0.0.0.0:9000"
export RUSTFS_CONSOLE_ENABLE="false"
export RUSTFS_VOLUMES="/data"

exec /entrypoint.sh rustfs
