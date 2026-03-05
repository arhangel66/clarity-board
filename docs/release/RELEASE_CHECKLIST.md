# Release Checklist

## Pre-release

- [ ] `backend` tests pass: `uv run pytest -q`
- [ ] `frontend` unit tests pass: `pnpm test -- --run`
- [ ] `frontend` build passes: `pnpm build`
- [ ] `frontend` type/svelte checks pass: `pnpm check`
- [ ] Relevant e2e suite passes
- [ ] `CHANGELOG.md` updated for release scope

## Data Safety

- [ ] Required migrations identified and executed
- [ ] DB backup created before deploy
- [ ] Restore path verified (at least once on non-prod)

## Deployment

- [ ] Commit merged to `main`
- [ ] CI green for target commit
- [ ] Deploy workflow completed successfully
- [ ] Health check green: `/api/health`

## Post-release

- [ ] Smoke test critical user path (login, session load, card CRUD)
- [ ] Verify logs for unexpected errors
- [ ] Note rollback command/path if incident appears

## Rollback Notes Template

- Trigger condition:
- Rollback method:
- Data impact:
- Follow-up action:
