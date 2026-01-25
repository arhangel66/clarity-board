/**
 * Auth fixture for E2E tests with dev bypass.
 *
 * Provides an authenticated page by navigating to /?dev=1
 * which triggers the frontend dev auth bypass.
 */
import { test as base, type Page, expect } from '@playwright/test';

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

    // Create a board if none exist
    const emptyMessage = page.locator('.boards-empty');
    const hasNoBoards = await emptyMessage.isVisible().catch(() => false);

    if (hasNoBoards) {
      console.log('[E2E Fixture] No boards found, creating one via API...');

      // Create board via API directly (more reliable than clicking)
      const response = await page.request.post('http://localhost:8000/api/sessions', {
        headers: {
          Authorization: 'Bearer dev-token',
        },
      });

      if (response.ok()) {
        const data = await response.json();
        console.log('[E2E Fixture] Board created:', data.session?.id);

        // Reload to fetch the new board
        await page.reload();
        await expect(page.locator('.boards-sidebar')).toBeVisible({ timeout: 10_000 });
        await expect(page.locator('.board-item').first()).toBeVisible({ timeout: 10_000 });
      } else {
        console.error('[E2E Fixture] Failed to create board:', response.status());
      }
    }

    // Select the first board if available
    const firstBoard = page.locator('.board-item').first();
    if (await firstBoard.isVisible({ timeout: 2_000 }).catch(() => false)) {
      await firstBoard.click();
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
