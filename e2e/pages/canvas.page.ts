/**
 * Page object for the Canvas component.
 */
import type { Page, Locator } from '@playwright/test';

export class CanvasPage {
  readonly page: Page;
  readonly container: Locator;
  readonly cardsContainer: Locator;
  readonly quickCreatePopover: Locator;
  readonly quickCreateTextarea: Locator;
  readonly quickCreateTypeSelect: Locator;
  readonly quickCreateSubmitBtn: Locator;

  constructor(page: Page) {
    this.page = page;
    this.container = page.locator('.canvas-container');
    this.cardsContainer = page.locator('.cards-container');
    this.quickCreatePopover = page.locator('.create-card-popover');
    this.quickCreateTextarea = page.locator('.create-card-text');
    this.quickCreateTypeSelect = page.locator('#quick-card-type');
    this.quickCreateSubmitBtn = page.locator('.create-card-btn.primary');
  }

  /**
   * Get all card elements on the canvas.
   */
  getAllCards(): Locator {
    return this.page.locator('.fact-card');
  }

  /**
   * Get a card by its text content.
   */
  getCardByText(text: string): Locator {
    return this.page.locator('.fact-card').filter({ hasText: text });
  }

  /**
   * Get a card by its ID.
   */
  getCardById(id: string): Locator {
    return this.page.locator(`.fact-card[data-card-id="${id}"]`);
  }

  /**
   * Get the card count.
   */
  async getCardCount(): Promise<number> {
    return await this.getAllCards().count();
  }

  /**
   * Click on a card to select it.
   */
  async selectCard(cardLocator: Locator): Promise<void> {
    await cardLocator.click({ force: true });
  }

  /**
   * Double-click to open quick create at a position.
   */
  async openQuickCreate(x: number, y: number): Promise<void> {
    await this.cardsContainer.dblclick({ position: { x, y } });
  }

  /**
   * Create a card via quick create form.
   */
  async createCardViaQuickCreate(
    text: string,
    type: string = 'fact',
  ): Promise<void> {
    // Open quick create at center-ish of canvas
    const box = await this.cardsContainer.boundingBox();
    if (!box) throw new Error('Canvas not visible');

    await this.openQuickCreate(box.width / 2, box.height / 2);
    await this.quickCreatePopover.waitFor({ state: 'visible' });

    // Select type
    await this.quickCreateTypeSelect.selectOption(type);

    // Enter text
    await this.quickCreateTextarea.fill(text);

    // Submit
    await this.quickCreateSubmitBtn.click();
  }

  /**
   * Wait for a card with specific text to appear.
   */
  async waitForCardWithText(text: string, timeout = 10_000): Promise<Locator> {
    const card = this.getCardByText(text);
    await card.waitFor({ state: 'visible', timeout });
    return card;
  }
}
