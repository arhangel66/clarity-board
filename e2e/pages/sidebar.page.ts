/**
 * Page object for the BoardsSidebar component.
 */
import type { Page, Locator } from '@playwright/test';

export class SidebarPage {
  readonly page: Page;
  readonly sidebar: Locator;
  readonly toggleButton: Locator;
  readonly appName: Locator;
  readonly newBoardButton: Locator;
  readonly boardsList: Locator;
  readonly logoutButton: Locator;
  readonly userName: Locator;
  readonly deleteButton: Locator;
  readonly legendSection: Locator;

  constructor(page: Page) {
    this.page = page;
    this.sidebar = page.locator('.boards-sidebar');
    this.toggleButton = this.sidebar.locator('.icon-btn');
    this.appName = page.locator('.app-logo');
    this.newBoardButton = page.locator('.new-board-row');
    this.boardsList = page.locator('.boards-list');
    this.logoutButton = page.locator('.logout-btn');
    this.userName = page.locator('.user-name');
    this.deleteButton = page.locator('.tool-btn.delete');
    this.legendSection = page.locator('.legend-section');
  }

  /**
   * Check if sidebar is collapsed.
   */
  async isCollapsed(): Promise<boolean> {
    return await this.sidebar.evaluate((el) =>
      el.classList.contains('collapsed'),
    );
  }

  /**
   * Toggle sidebar visibility.
   */
  async toggle(): Promise<void> {
    const collapsed = await this.isCollapsed();
    if (collapsed) {
      await this.page.locator('.collapsed-toggle').click();
    } else {
      await this.toggleButton.click();
    }
  }

  /**
   * Get all board items.
   */
  getBoardItems(): Locator {
    return this.page.locator('.board-item');
  }

  /**
   * Get the active board item.
   */
  getActiveBoard(): Locator {
    return this.page.locator('.board-item.active');
  }

  /**
   * Select a board by its title.
   */
  async selectBoardByTitle(title: string): Promise<void> {
    await this.getBoardItems().filter({ hasText: title }).click();
  }

  /**
   * Create a new board.
   */
  async createNewBoard(): Promise<void> {
    await this.newBoardButton.click();
  }

  /**
   * Click delete button (for selected cards).
   */
  async clickDeleteButton(): Promise<void> {
    await this.deleteButton.click();
  }

  /**
   * Get the selection count text.
   */
  getSelectionSection(): Locator {
    return this.page.locator('.selection-section');
  }
}
