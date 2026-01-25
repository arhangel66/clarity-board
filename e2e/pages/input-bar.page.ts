/**
 * Page object for the InputBar component.
 */
import type { Page, Locator } from '@playwright/test';

export class InputBarPage {
  readonly page: Page;
  readonly inputDock: Locator;
  readonly capsule: Locator;
  readonly textInput: Locator;
  readonly sendButton: Locator;
  readonly toggleButton: Locator;
  readonly micButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.inputDock = page.locator('.input-dock');
    this.capsule = page.locator('.capsule');
    this.textInput = page.locator('.text-input');
    this.sendButton = page.locator('.send-btn');
    this.toggleButton = page.locator('.utility-btn');
    this.micButton = page.locator('.mic-btn');
  }

  /**
   * Check if voice mode is active.
   */
  async isVoiceMode(): Promise<boolean> {
    return await this.micButton.isVisible();
  }

  /**
   * Switch to text input mode.
   */
  async switchToTextMode(): Promise<void> {
    if (await this.isVoiceMode()) {
      await this.toggleButton.click();
      await this.textInput.waitFor({ state: 'visible' });
    }
  }

  /**
   * Switch to voice mode.
   */
  async switchToVoiceMode(): Promise<void> {
    if (!(await this.isVoiceMode())) {
      await this.toggleButton.first().click();
      await this.micButton.waitFor({ state: 'visible' });
    }
  }

  /**
   * Send a text message via the input bar.
   */
  async sendText(text: string): Promise<void> {
    await this.switchToTextMode();
    await this.textInput.fill(text);
    await this.sendButton.click();
  }

  /**
   * Send text by pressing Enter.
   */
  async sendTextWithEnter(text: string): Promise<void> {
    await this.switchToTextMode();
    await this.textInput.fill(text);
    await this.textInput.press('Enter');
  }
}
