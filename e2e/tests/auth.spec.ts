/**
 * Auth flow E2E tests.
 *
 * Tests the landing page and dev auth bypass.
 */
import { test, expect } from '@playwright/test';
import { test as authenticatedTest } from '../fixtures/auth.fixture';
import { SidebarPage } from '../pages/sidebar.page';

test.describe('Authentication', () => {
  test('landing page shows login button', async ({ page }) => {
    // Navigate without dev bypass
    await page.goto('/');

    // Landing page should be visible
    const landingSection = page.locator('.landing-root');
    await expect(landingSection).toBeVisible();

    // CTA button should be present (nav or hero)
    const ctaButton = page.locator('.nav-cta, .hero-cta').first();
    await expect(ctaButton).toBeVisible();
  });

  test('dev bypass authenticates and shows workspace', async ({ page }) => {
    // Navigate with dev bypass
    await page.goto('/?dev=1');

    // Should skip landing and show main app
    const sidebar = new SidebarPage(page);
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // App name should be visible
    await expect(sidebar.appName).toHaveText('Clarify Board');

    // Canvas should be visible (workspace loaded)
    const canvas = page.locator('.canvas-container');
    await expect(canvas).toBeVisible();
  });

  test('dev user can see boards section', async ({ page }) => {
    await page.goto('/?dev=1');

    const sidebar = new SidebarPage(page);
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // The boards section may show an empty state before any board exists
    await expect(page.locator('.boards-empty, .board-item').first()).toBeVisible();

    // New board button should be clickable
    await expect(sidebar.newBoardButton).toBeEnabled();
  });
});

authenticatedTest.describe('Authenticated Session Recovery', () => {
  authenticatedTest('dev bypass survives a page reload on a real board', async ({ authenticatedPage }) => {
    const sidebar = new SidebarPage(authenticatedPage);

    await expect(sidebar.getActiveBoard()).toBeVisible({ timeout: 10_000 });
    await expect(authenticatedPage.locator('.canvas-container')).toBeVisible();

    await authenticatedPage.reload();

    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });
    await expect(sidebar.getActiveBoard()).toBeVisible({ timeout: 10_000 });
    await expect(authenticatedPage.locator('.canvas-container')).toBeVisible();
  });

  authenticatedTest('dev bypass reopens the workspace without returning to landing', async ({ authenticatedPage }) => {
    const context = authenticatedPage.context();
    const sidebar = new SidebarPage(authenticatedPage);

    await expect(sidebar.getBoardItems().first()).toBeVisible({ timeout: 10_000 });
    await authenticatedPage.close();

    const reopenedPage = await context.newPage();
    const reopenedSidebar = new SidebarPage(reopenedPage);

    await reopenedPage.goto('/?dev=1');

    await expect(reopenedSidebar.sidebar).toBeVisible({ timeout: 10_000 });
    await expect(reopenedSidebar.getBoardItems().first()).toBeVisible({ timeout: 10_000 });
    await expect(reopenedPage.locator('.canvas-container')).toBeVisible({ timeout: 10_000 });
    await expect(reopenedPage.locator('.landing-root')).toHaveCount(0);
  });
});
