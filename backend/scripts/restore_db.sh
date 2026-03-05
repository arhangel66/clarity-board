#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: restore_db.sh <backup_file> [target_db_path]" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_FILE="$1"
TARGET_DB="${2:-$ROOT_DIR/data/fact_cards.db}"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Backup file not found: $BACKUP_FILE" >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET_DB")"

if [[ -f "$TARGET_DB" ]]; then
  SAFETY_COPY="$TARGET_DB.pre-restore.$(date -u +%Y%m%dT%H%M%SZ).bak"
  cp "$TARGET_DB" "$SAFETY_COPY"
  echo "Created safety backup: $SAFETY_COPY"
fi

cp "$BACKUP_FILE" "$TARGET_DB"
echo "Restored DB: $TARGET_DB"

if command -v sqlite3 >/dev/null 2>&1; then
  INTEGRITY="$(sqlite3 "$TARGET_DB" "PRAGMA integrity_check;" | tr -d '\r')"
  if [[ "$INTEGRITY" != "ok" ]]; then
    echo "Integrity check failed: $INTEGRITY" >&2
    exit 1
  fi
  echo "Integrity check: ok"
else
  echo "sqlite3 not found, integrity check skipped."
fi
