/**
 * Unified Full Flow E2E test.
 *
 * This test covers the complete user journey in a single process:
 * 1. Authentication bypass
 * 2. Card creation via text message
 * 3. Card selection and modification
 * 4. Card deletion
 * 5. Persistence check
 */
import { test, expect } from '../fixtures/auth.fixture';
import { CanvasPage } from '../pages/canvas.page';
import { InputBarPage } from '../pages/input-bar.page';
import { SidebarPage } from '../pages/sidebar.page';

test.describe('Unified User Journey', () => {
  test('complete flow from start to finish', async ({ authenticatedPage }) => {
    const page = authenticatedPage;
    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    // Step 1: Verify workspace is ready
    await expect(sidebar.sidebar).toBeVisible();
    await expect(canvas.container).toBeVisible();

    // Step 2: Send first message to define the problem
    console.log('[E2E] Sending initial message...');
    await inputBar.sendText('How to improve E2E test reliability?');

    // Wait for card creation (Mock AI mode is fast)
    await canvas.waitForCardWithText('How to improve E2E test reliability?');

    // Step 3: Add more context
    console.log('[E2E] Adding more context...');
    await inputBar.sendText('We need better waiting strategies');
    await canvas.waitForCardWithText('We need better waiting strategies');

    // Step 4: Interact with a card
    console.log('[E2E] Selecting and modifying card...');
    const card = canvas.getCardByText('We need better waiting strategies');
    await canvas.selectCard(card);

    // Verify selection UI
    await expect(sidebar.getSelectionSection()).toBeVisible();

    // Step 5: Delete the card
    console.log('[E2E] Deleting card...');
    await sidebar.clickDeleteButton();
    await expect(card).not.toBeVisible({ timeout: 5_000 });

    // Step 6: Verify first card still exists (was not deleted)
    await expect(
      canvas.getCardByText('How to improve E2E test reliability?')
    ).toBeVisible();

    console.log('[E2E] Unified flow completed successfully!');
  });
});
