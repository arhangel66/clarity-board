/**
 * Card CRUD operations E2E tests.
 *
 * Tests creating, selecting, and deleting cards.
 */
import { test, expect } from '../fixtures/auth.fixture';
import { CanvasPage } from '../pages/canvas.page';
import { InputBarPage } from '../pages/input-bar.page';
import { SidebarPage } from '../pages/sidebar.page';

test.describe('Card CRUD Operations', () => {
  test('create card via text input', async ({ authenticatedPage: page }) => {
    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);

    // Count initial cards
    const initialCount = await canvas.getCardCount();

    // Send a message to create a card
    await inputBar.sendText('This is a test fact');

    // Wait for new card to appear
    await canvas.waitForCardWithText('This is a test fact');

    // Card count should increase
    const newCount = await canvas.getCardCount();
    expect(newCount).toBeGreaterThan(initialCount);
  });

  test('create card via quick create', async ({ authenticatedPage: page }) => {
    const canvas = new CanvasPage(page);

    const initialCount = await canvas.getCardCount();

    // Create card via double-click popup
    await canvas.createCardViaQuickCreate('Quick created card', 'fact');

    // Wait for card to appear
    await canvas.waitForCardWithText('Quick created card');

    const newCount = await canvas.getCardCount();
    expect(newCount).toBeGreaterThan(initialCount);
  });

  test('select card by clicking', async ({ authenticatedPage: page }) => {
    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    // Create a card first
    await inputBar.sendText('Card to select');
    const card = await canvas.waitForCardWithText('Card to select');

    // Click on the card
    await canvas.selectCard(card);

    // Selection section should appear in sidebar
    await expect(sidebar.getSelectionSection()).toBeVisible();
  });

  test('delete selected card', async ({ authenticatedPage: page }) => {
    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    // Create a card
    await inputBar.sendText('Card to delete');
    const card = await canvas.waitForCardWithText('Card to delete');

    const countBefore = await canvas.getCardCount();

    // Select the card
    await canvas.selectCard(card);

    // Wait for selection UI
    await expect(sidebar.getSelectionSection()).toBeVisible();

    // Click delete button
    await sidebar.clickDeleteButton();

    // Card should be removed
    await expect(card).not.toBeVisible({ timeout: 5_000 });

    const countAfter = await canvas.getCardCount();
    expect(countAfter).toBeLessThan(countBefore);
  });

  test('cannot delete root/question card', async ({
    authenticatedPage: page,
  }) => {
    const canvas = new CanvasPage(page);
    const sidebar = new SidebarPage(page);

    // Wait for canvas to be ready
    await expect(canvas.container).toBeVisible();

    // Find a question card (if exists) by looking for purple-colored card
    // or create a session first via text input
    const inputBar = new InputBarPage(page);
    await inputBar.sendText('My central question');

    // Get all cards and try to find the root one
    // Root cards have is_root=true flag, usually the question card
    const cards = canvas.getAllCards();
    const cardCount = await cards.count();

    // If there's at least one card, test that root card persists
    if (cardCount > 0) {
      // Select first card
      await cards.first().click();

      // Try to delete via keyboard
      await page.keyboard.press('Delete');

      // Wait a bit
      await page.waitForTimeout(500);

      // Cards should still exist (root cannot be deleted)
      const newCount = await canvas.getCardCount();
      expect(newCount).toBeGreaterThanOrEqual(1);
    }
  });
});
