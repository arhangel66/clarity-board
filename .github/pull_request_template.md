## Summary

- What changed?
- Why this change?

## Validation

- [ ] `cd backend && uv run pytest -q`
- [ ] `cd frontend && pnpm test -- --run`
- [ ] `cd frontend && pnpm build`
- [ ] `cd frontend && pnpm check`
- [ ] Relevant e2e tests passed (if UI/protocol changed)

## Quality Checklist

- [ ] No secrets or local artifacts were committed
- [ ] WebSocket/API contract changes are documented
- [ ] `CHANGELOG.md` updated (if user-visible or operational change)
- [ ] Architecture docs/ADR updated (if architectural decision changed)

## Rollout Notes

- [ ] Migration needed
- [ ] Backup/restore impact reviewed
- [ ] Rollback approach documented
