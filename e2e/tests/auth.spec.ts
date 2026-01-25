/**
 * Auth flow E2E tests.
 *
 * Tests the landing page and dev auth bypass.
 */
import { test, expect } from '@playwright/test';
import { SidebarPage } from '../pages/sidebar.page';

test.describe('Authentication', () => {
  test('landing page shows login button', async ({ page }) => {
    // Navigate without dev bypass
    await page.goto('/');

    // Landing page should be visible
    const landingSection = page.locator('.landing');
    await expect(landingSection).toBeVisible();

    // CTA button should be present
    const ctaButton = page.locator('.cta-btn');
    await expect(ctaButton).toBeVisible();
  });

  test('dev bypass authenticates and shows workspace', async ({ page }) => {
    // Navigate with dev bypass
    await page.goto('/?dev=1');

    // Should skip landing and show main app
    const sidebar = new SidebarPage(page);
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // App name should be visible
    await expect(sidebar.appName).toHaveText('Fact Cards');

    // Canvas should be visible (workspace loaded)
    const canvas = page.locator('.canvas-container');
    await expect(canvas).toBeVisible();
  });

  test('dev user can see boards section', async ({ page }) => {
    await page.goto('/?dev=1');

    const sidebar = new SidebarPage(page);
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // Boards list should be present
    await expect(sidebar.boardsList).toBeVisible();

    // New board button should be clickable
    await expect(sidebar.newBoardButton).toBeEnabled();
  });
});
