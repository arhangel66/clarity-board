/**
 * Auth fixture for E2E tests with dev bypass.
 *
 * Provides an authenticated page by navigating to /?dev=1
 * which triggers the frontend dev auth bypass.
 */
import { test as base, type Page, expect } from '@playwright/test';

const PLAYWRIGHT_API_BASE =
  process.env.PLAYWRIGHT_API_BASE ?? 'http://127.0.0.1:18000';

/**
 * Extended test fixtures with auth-related helpers.
 */
export interface AuthFixtures {
  /** Page authenticated via dev bypass */
  authenticatedPage: Page;
}

/**
 * Test fixture that provides an authenticated page.
 */
export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Set localStorage to skip onboarding before navigating
    await page.addInitScript(() => {
      localStorage.setItem('fact_onboarding_seen', '1');
    });

    // Navigate with dev bypass param
    await page.goto('/?dev=1');

    // Wait for auth to complete and app to render
    // The sidebar should appear after successful auth
    await expect(page.locator('.boards-sidebar')).toBeVisible({ timeout: 10_000 });

    // Dismiss onboarding if it's still shown (fallback)
    const skipButton = page.locator('.skip-btn');
    if (await skipButton.isVisible({ timeout: 1_000 }).catch(() => false)) {
      await skipButton.click();
    }

    // Wait for boards to finish loading (loading indicator disappears)
    // The sidebar shows either boards list or "No boards yet" after loading
    await expect(
      page.locator('.boards-empty, .board-item').first()
    ).toBeVisible({ timeout: 10_000 });

    // Wait a bit for auth token to propagate through Svelte effects
    await page.waitForTimeout(500);

    // Always create a fresh board for test isolation
    // (each test gets its own empty board so cards don't leak between tests)
    console.log('[E2E Fixture] Creating fresh board for test isolation...');
    const response = await page.request.post(`${PLAYWRIGHT_API_BASE}/api/sessions`, {
      headers: {
        Authorization: 'Bearer dev-token',
      },
    });

    if (!response.ok()) {
      throw new Error(
        `[E2E Fixture] Failed to create board: ${response.status()} ${response.statusText()}`
      );
    }

    const data = await response.json();
    console.log('[E2E Fixture] Board created:', data.session?.id);

    // Reload to fetch the new board
    await page.reload();
    await expect(page.locator('.boards-sidebar')).toBeVisible({ timeout: 10_000 });
    await expect(page.locator('.board-item').first()).toBeVisible({ timeout: 10_000 });

    // Select the first board (the newest board is sorted to the top)
    const boardItems = page.locator('.board-item');
    const newestBoard = boardItems.first();
    if (await newestBoard.isVisible({ timeout: 2_000 }).catch(() => false)) {
      const isAlreadyActive = await newestBoard.evaluate((node) =>
        node.classList.contains('active')
      );
      if (!isAlreadyActive) {
        await newestBoard.scrollIntoViewIfNeeded();
        await newestBoard.click();
      }
      await expect(page.locator('.board-item.active')).toBeVisible({ timeout: 5_000 });
    }

    // Wait for canvas to be ready
    await expect(page.locator('.canvas-container')).toBeVisible({ timeout: 10_000 });

    // Wait for WebSocket connection to establish
    await page.waitForTimeout(500);

    await use(page);
  },
});

export { expect } from '@playwright/test';
