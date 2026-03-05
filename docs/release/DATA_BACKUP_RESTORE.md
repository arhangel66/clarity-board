# Data Backup and Restore Runbook

Last updated: 2026-03-05

## Database Path

Default runtime DB path:

- `backend/data/fact_cards.db`

## Backup

```bash
bash backend/scripts/backup_db.sh
```

Optional arguments:

```bash
bash backend/scripts/backup_db.sh <db_path> <backup_dir>
```

## Restore

```bash
bash backend/scripts/restore_db.sh <backup_file>
```

Optional target DB path:

```bash
bash backend/scripts/restore_db.sh <backup_file> <target_db_path>
```

Behavior:

- Creates a pre-restore safety copy if target DB already exists.
- Runs `PRAGMA integrity_check` when `sqlite3` is available.

## Restore Smoke Test (non-prod copy)

```bash
bash backend/scripts/restore_smoke.sh <backup_file>
```

Optional target copy path:

```bash
bash backend/scripts/restore_smoke.sh <backup_file> <target_copy_path>
```

This validates that backup can be restored and the `sessions` table is readable.

## Managed Migrations

Run managed migrations against default DB:

```bash
python backend/scripts/migrate.py
```

Custom DB path:

```bash
python backend/scripts/migrate.py --db-path /path/to/fact_cards.db
```

## Operational Notes

- Always create backup before running schema changes.
- Never run restore directly on prod first; run smoke restore on a copy.
- Record backup filename and time in release notes.
