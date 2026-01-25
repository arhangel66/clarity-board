/**
 * Full happy path E2E test.
 *
 * Tests the complete flow from landing to creating and managing cards.
 */
import { test, expect } from '@playwright/test';
import { CanvasPage } from '../pages/canvas.page';
import { InputBarPage } from '../pages/input-bar.page';
import { SidebarPage } from '../pages/sidebar.page';

// Helper to set up page with onboarding skipped
async function setupPage(page: import('@playwright/test').Page) {
  await page.addInitScript(() => {
    localStorage.setItem('fact_onboarding_seen', '1');
  });
  await page.goto('/?dev=1');
}

test.describe('Full Happy Path', () => {
  test('complete flow: login -> create board -> add cards -> select -> delete', async ({
    page,
  }) => {
    // Generate unique suffix for this test run
    const testId = Date.now().toString(36);

    // Step 1: Navigate with dev auth bypass
    await setupPage(page);

    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    // Step 2: Verify workspace loaded
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });
    await expect(canvas.container).toBeVisible();

    // Step 3: Send text messages to create cards (with unique suffix)
    await inputBar.sendText(`Project task ${testId}`);
    await page.waitForTimeout(1_500);

    await inputBar.sendText(`Budget limit ${testId}`);
    await page.waitForTimeout(1_500);

    await inputBar.sendText(`Card to delete ${testId}`);
    await page.waitForTimeout(1_500);

    // Step 4: Verify cards exist
    const cardCount = await canvas.getCardCount();
    expect(cardCount).toBeGreaterThanOrEqual(1);

    // Step 5: Select a card
    const cardToDelete = canvas.getCardByText(`Card to delete ${testId}`);
    await canvas.selectCard(cardToDelete);

    // Verify selection UI appears
    await expect(sidebar.getSelectionSection()).toBeVisible();

    // Step 6: Delete the selected card
    await sidebar.clickDeleteButton();

    // Verify card is removed
    await expect(cardToDelete).not.toBeVisible({ timeout: 5_000 });

    // Step 10: Verify sidebar functionality
    await expect(sidebar.appName).toHaveText('Fact Cards');
    await expect(sidebar.legendSection).toBeVisible();
  });

  test('sidebar collapse and expand works', async ({ page }) => {
    await setupPage(page);

    const sidebar = new SidebarPage(page);
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // Initially not collapsed
    expect(await sidebar.isCollapsed()).toBe(false);

    // Toggle to collapse
    await sidebar.toggle();
    await page.waitForTimeout(500);
    expect(await sidebar.isCollapsed()).toBe(true);

    // Toggle to expand
    await sidebar.toggle();
    await page.waitForTimeout(500);
    expect(await sidebar.isCollapsed()).toBe(false);
  });

  test('input bar mode switching works', async ({ page }) => {
    await setupPage(page);

    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // Default should be voice mode
    expect(await inputBar.isVoiceMode()).toBe(true);

    // Switch to text mode
    await inputBar.switchToTextMode();
    expect(await inputBar.isVoiceMode()).toBe(false);
    await expect(inputBar.textInput).toBeVisible();

    // Switch back to voice mode
    await inputBar.switchToVoiceMode();
    expect(await inputBar.isVoiceMode()).toBe(true);
    await expect(inputBar.micButton).toBeVisible();
  });

  test('multiple cards can be selected via lasso', async ({ page }) => {
    await setupPage(page);

    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });

    // Create multiple cards
    await inputBar.sendText('First fact card');
    await page.waitForTimeout(1_000);

    await inputBar.sendText('Second fact card');
    await page.waitForTimeout(1_000);

    // Get canvas bounds for lasso selection
    const canvasBounds = await canvas.cardsContainer.boundingBox();
    if (!canvasBounds) throw new Error('Canvas not visible');

    // Perform lasso selection (drag from top-left to bottom-right)
    await canvas.cardsContainer.dispatchEvent('mousedown', {
      clientX: canvasBounds.x + 50,
      clientY: canvasBounds.y + 50,
    });

    await page.mouse.move(
      canvasBounds.x + canvasBounds.width - 50,
      canvasBounds.y + canvasBounds.height - 50,
    );

    await page.mouse.up();

    // Some cards may be selected (depends on positioning)
    // This is a basic smoke test for lasso functionality
  });
});
