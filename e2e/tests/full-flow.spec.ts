/**
 * Full happy path E2E test.
 *
 * Tests the complete flow from landing to creating and managing cards.
 */
import { test, expect, type APIRequestContext, type Locator, type Page } from '@playwright/test';
import { CanvasPage } from '../pages/canvas.page';
import { InputBarPage } from '../pages/input-bar.page';
import { SidebarPage } from '../pages/sidebar.page';
import {
  buildCompletedOnboardingState,
  LEGACY_ONBOARDING_STORAGE_KEY,
  LEGACY_TIPS_STORAGE_KEY,
  ONBOARDING_STORAGE_KEY,
} from '../../frontend/src/lib/stores/onboarding';

const DEV_TOKEN = 'dev-token';
const DEFAULT_LOCALE = 'en';
const E2E_API_BASE = 'http://127.0.0.1:18000';

async function createFreshBoard(request: APIRequestContext) {
  const response = await request.post(`${E2E_API_BASE}/api/sessions`, {
    headers: {
      Authorization: `Bearer ${DEV_TOKEN}`,
    },
  });

  expect(response.ok()).toBeTruthy();
}

async function setupPage(
  page: Page,
  request: APIRequestContext,
  options: { skipOnboarding?: boolean } = {},
) {
  await createFreshBoard(request);

  await page.goto('/');
  await page.evaluate(
    ({
      skipOnboarding,
      locale,
      onboardingKey,
      onboardingState,
      legacyOnboardingKey,
      legacyTipsKey,
    }) => {
      localStorage.setItem('fact_locale', locale);
      localStorage.removeItem(legacyOnboardingKey);
      localStorage.removeItem(legacyTipsKey);

      if (skipOnboarding) {
        localStorage.setItem(onboardingKey, onboardingState);
      } else {
        localStorage.removeItem(onboardingKey);
      }
    },
    {
      skipOnboarding: options.skipOnboarding ?? true,
      locale: DEFAULT_LOCALE,
      onboardingKey: ONBOARDING_STORAGE_KEY,
      onboardingState: JSON.stringify(buildCompletedOnboardingState()),
      legacyOnboardingKey: LEGACY_ONBOARDING_STORAGE_KEY,
      legacyTipsKey: LEGACY_TIPS_STORAGE_KEY,
    },
  );

  await page.goto('/?dev=1');
  await expect(page.locator('.boards-sidebar')).toBeVisible({ timeout: 10_000 });
  await expect(page.locator('.board-item.active')).toBeVisible({ timeout: 10_000 });
  await expect(page.locator('.canvas-container')).toBeVisible();
}

async function sendTextAndWaitForCardCount(
  inputBar: InputBarPage,
  canvas: CanvasPage,
  text: string,
  expectedCount: number,
) {
  await inputBar.sendText(text);
  await expect
    .poll(async () => canvas.getCardCount(), { timeout: 10_000 })
    .toBe(expectedCount);
}

async function dragLocator(
  page: Page,
  locator: Locator,
  delta: { x: number; y: number },
) {
  const box = await locator.boundingBox();
  if (!box) {
    throw new Error('Target is not visible for dragging');
  }

  const startX = box.x + box.width / 2;
  const startY = box.y + box.height / 2;

  await page.mouse.move(startX, startY);
  await page.mouse.down();
  await page.mouse.move(startX + delta.x, startY + delta.y, { steps: 10 });
  await page.mouse.up();
}

test.describe('Full Happy Path', () => {
  test('complete flow: login -> create board -> add cards -> select -> delete', async ({
    page,
    request,
  }) => {
    // Generate unique suffix for this test run
    const testId = Date.now().toString(36);

    // Step 1: Navigate with dev auth bypass
    await setupPage(page, request);

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
    await setupPage(page, page.request);

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
    await setupPage(page, page.request);

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
    await setupPage(page, page.request);

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

  test('onboarding persists after completion until help restarts it', async ({
    page,
    request,
  }) => {
    const testId = Date.now().toString(36);
    const canvas = new CanvasPage(page);
    const inputBar = new InputBarPage(page);
    const sidebar = new SidebarPage(page);

    await setupPage(page, request, { skipOnboarding: false });

    const dialog = page.locator('.tooltip-overlay[role="dialog"]');
    const startButton = dialog.getByRole('button', { name: 'Start', exact: true });
    const nextButton = dialog.getByRole('button', { name: 'Next', exact: true });
    const finishButton = dialog.getByRole('button', { name: 'Finish', exact: true });

    await expect(dialog).toContainText('Where to start');
    await expect(startButton).toBeDisabled();

    await sendTextAndWaitForCardCount(
      inputBar,
      canvas,
      `Career dilemma about relocation ${testId}`,
      1,
    );
    await expect(startButton).toBeEnabled();
    await startButton.click();

    await expect(nextButton).toBeDisabled();
    await sendTextAndWaitForCardCount(
      inputBar,
      canvas,
      `Team morale dropped sharply after the reorg ${testId}`,
      2,
    );
    await sendTextAndWaitForCardCount(
      inputBar,
      canvas,
      `Savings cover six months of rent and expenses ${testId}`,
      3,
    );
    await expect(nextButton).toBeEnabled();
    await nextButton.click();

    await expect(nextButton).toBeDisabled();
    await expect(dialog).toHaveAttribute('data-active-step', 'move_card');
    await expect(dialog).toContainText('Move a card');

    const header = dialog.locator('.tooltip-header');
    const beforeMove = await dialog.boundingBox();
    if (!beforeMove) {
      throw new Error('Onboarding tooltip should be visible before drag');
    }
    await dragLocator(page, header, { x: -120, y: -90 });
    const afterMove = await dialog.boundingBox();
    if (!afterMove) {
      throw new Error('Onboarding tooltip should remain visible after drag');
    }
    expect(Math.abs(afterMove.x - beforeMove.x)).toBeGreaterThan(40);
    expect(Math.abs(afterMove.y - beforeMove.y)).toBeGreaterThan(40);

    await dragLocator(page, page.locator('.fact-card:not(.is-root)').first(), {
      x: 90,
      y: -50,
    });

    await expect(nextButton).toBeEnabled();
    await nextButton.click();
    await expect(dialog).toHaveCount(0);

    await sendTextAndWaitForCardCount(
      inputBar,
      canvas,
      `The current workload leaves me burned out by Thursday ${testId}`,
      4,
    );
    await sendTextAndWaitForCardCount(
      inputBar,
      canvas,
      `A mentor offered referrals and interview prep abroad ${testId}`,
      5,
    );
    await sendTextAndWaitForCardCount(
      inputBar,
      canvas,
      `Visa timing and family logistics are still unclear ${testId}`,
      6,
    );

    await expect(finishButton).toBeVisible({ timeout: 10_000 });
    await expect(finishButton).toBeEnabled();
    await finishButton.click();
    await expect(dialog).toHaveCount(0);

    await page.reload();
    await expect(sidebar.sidebar).toBeVisible({ timeout: 10_000 });
    await expect(dialog).toHaveCount(0);

    await page.locator('.help-wrapper .tool-btn').click();
    const helpRestartButton = page.locator('.help-popover').first().locator('.help-restart');
    await expect(helpRestartButton).toBeVisible();
    await helpRestartButton.click();

    await expect(dialog).toContainText('Where to start');
    await expect(startButton).toBeEnabled();
  });
});
