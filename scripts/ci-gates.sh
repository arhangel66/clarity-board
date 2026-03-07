#!/usr/bin/env bash
set -euo pipefail

# CI Gates — local mirror of GitHub Actions E2E workflow
# Usage: ./scripts/ci-gates.sh [--skip-e2e]

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

SKIP_E2E=false
[[ "${1:-}" == "--skip-e2e" ]] && SKIP_E2E=true

BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m'

step() {
  echo -e "\n${BOLD}==> $1${RESET}"
}

fail() {
  echo -e "\n${RED}FAIL: $1${RESET}"
  exit 1
}

# 1) Backend tests
step "Backend pytest"
(cd backend && uv run pytest -q) || fail "backend pytest"

# 2) Frontend unit tests
step "Frontend unit tests"
(cd frontend && pnpm test -- --run) || fail "frontend unit tests"

# 3) Frontend build
step "Frontend build"
(cd frontend && pnpm build) || fail "frontend build (Vite)"

# 4) Frontend svelte-check (typecheck + lint)
step "Frontend svelte-check"
(cd frontend && pnpm check) || fail "frontend svelte-check"

# 5) E2E tests
if [ "$SKIP_E2E" = true ]; then
  step "E2E tests (skipped)"
else
  step "E2E tests"
  # Clean DB to ensure test isolation (CI also starts with empty DB)
  rm -f backend/data/fact_cards.db
  # CI=true ensures Playwright starts fresh servers (no reuseExistingServer)
  # matching GitHub Actions behavior exactly
  CI=true DEV_AUTH_BYPASS=true AI_MOCK_MODE=true pnpm e2e || fail "E2E tests"
fi

echo -e "\n${GREEN}${BOLD}All CI gates passed${RESET}"
