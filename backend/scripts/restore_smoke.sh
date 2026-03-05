#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: restore_smoke.sh <backup_file> [target_copy_path]" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_FILE="$1"
TARGET_COPY="${2:-$ROOT_DIR/data/fact_cards.restore-smoke.db}"

"$ROOT_DIR/scripts/restore_db.sh" "$BACKUP_FILE" "$TARGET_COPY"

if command -v sqlite3 >/dev/null 2>&1; then
  SESSION_COUNT="$(sqlite3 "$TARGET_COPY" "SELECT COUNT(*) FROM sessions;")"
  echo "Restore smoke OK. sessions_count=$SESSION_COUNT target=$TARGET_COPY"
else
  echo "Restore smoke completed (sqlite3 unavailable for session count). target=$TARGET_COPY"
fi
