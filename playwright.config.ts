import { defineConfig, devices } from '@playwright/test';

/**
 * E2E tests configuration for Fact Card System.
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './e2e/tests',

  /* Run tests in files in parallel */
  fullyParallel: true,

  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,

  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,

  /* Opt out of parallel tests on CI (single worker for stability) */
  workers: process.env.CI ? 1 : undefined,

  /* Reporter to use */
  reporter: process.env.CI
    ? [['html', { outputFolder: 'playwright-report' }], ['github']]
    : [['html', { outputFolder: 'playwright-report' }]],

  /* Shared settings for all the projects below */
  use: {
    /* Base URL - frontend dev server */
    baseURL: 'http://127.0.0.1:4173',

    /* Collect trace when retrying the failed test */
    trace: 'on-first-retry',

    /* Screenshot on failure */
    screenshot: 'only-on-failure',

    /* Video on failure */
    video: 'on-first-retry',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  /* Run local dev servers before starting the tests */
  webServer: [
    {
      command:
        'rm -rf /tmp/fact-playwright-data && mkdir -p /tmp/fact-playwright-data && cd backend && FACT_DATA_DIR=/tmp/fact-playwright-data uv run uvicorn app.main:app --host 127.0.0.1 --port 18000',
      url: 'http://127.0.0.1:18000/api/health',
      reuseExistingServer: false,
      timeout: 60_000,
      env: {
        DEV_AUTH_BYPASS: 'true',
        AI_MOCK_MODE: 'true',
        E2E_UNLIMITED_ACCESS: 'true',
      },
    },
    {
      command:
        'cd frontend && VITE_API_BASE=http://127.0.0.1:18000 VITE_WS_BASE=ws://127.0.0.1:18000 pnpm dev --host 127.0.0.1 --port 4173',
      url: 'http://127.0.0.1:4173',
      reuseExistingServer: false,
      timeout: 60_000,
    },
  ],
});
