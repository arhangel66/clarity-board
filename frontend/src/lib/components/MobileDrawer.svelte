<script lang="ts">
  import { isDrawerOpen, closeDrawer } from '../stores/drawer';
  import { cards } from '../stores/cards';
  import {
    ONBOARDING_STEP_ORDER,
    onboarding,
    type OnboardingStepId
  } from '../stores/onboarding';
  import { zoom, ZOOM_MAX, ZOOM_MIN } from '../stores/zoom';
  import { availableLocales, locale, setLocale, strings } from '../stores/i18n';
  import { websocket } from '../stores/websocket';
  import { openCardDetail } from '../stores/cardDetail';
  import { auth } from '../stores/auth';
  import { boards } from '../stores/boards';
  import type { Locale } from '../stores/i18n';
  import type { Card } from '../types';

  const hasSession = websocket.hasSession;
  const STEP_INDEX: Record<OnboardingStepId, number> = {
    question: 0,
    cards: 1,
    move_card: 2,
    blind_spots: 3
  };

  let cardList = $state<Card[]>([]);
  let authToken = $state<string | null>(null);
  let activeStep = $state<OnboardingStepId | null>(null);
  let isTourComplete = $state(false);

  $effect(() => {
    const unsubscribe = cards.subscribe((list) => {
      cardList = list;
    });
    return unsubscribe;
  });

  $effect(() => {
    const unsubscribe = auth.subscribe((state) => {
      authToken = state.token;
    });
    return unsubscribe;
  });

  $effect(() => {
    const unsubscribe = onboarding.subscribe((state) => {
      activeStep = state.activeStep;
      isTourComplete = state.isTourComplete;
    });
    return unsubscribe;
  });

  function handleLanguageSelect(code: Locale) {
    setLocale(code);
  }

  async function handleNewSession() {
    if (!authToken) return;
    const board = await boards.createBoard(authToken);
    if (!board) return;
    closeDrawer();
  }

  function handleCardClick(cardId: string) {
    openCardDetail(cardId);
    closeDrawer();
  }

  function handleBoardSelect(boardId: string) {
    boards.setActiveBoard(boardId);
    closeDrawer();
  }

  function handleScrimClick() {
    closeDrawer();
  }

  function restartTutorial() {
    onboarding.restart();
    closeDrawer();
  }

  function getTourSummary(): string {
    if (activeStep) {
      return `${$strings.onboarding.steps[STEP_INDEX[activeStep]].title} · ${STEP_INDEX[activeStep] + 1}/${ONBOARDING_STEP_ORDER.length}`;
    }
    if (isTourComplete) {
      return $strings.onboarding.completed;
    }
    return $strings.onboarding.steps[0].title;
  }

  function getCardTypeColor(type: string): string {
    const colors: Record<string, string> = {
      question: 'var(--question-purple)',
      fact: 'var(--fact-blue)',
      pain: 'var(--pain-red)',
      resource: 'var(--resource-green)',
      hypothesis: 'var(--hypothesis-amber)',
      todo: 'var(--todo-teal)'
    };
    return colors[type] || 'var(--text-light)';
  }
</script>

{#if $isDrawerOpen}
  <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
  <div class="drawer-scrim" onclick={handleScrimClick}></div>
{/if}

<div class="drawer" class:open={$isDrawerOpen}>
  <div class="drawer-header">
    <span class="drawer-title">{$strings.drawer?.title || 'Menu'}</span>
    <button class="close-btn" onclick={closeDrawer} aria-label="Close menu">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
  </div>

  <div class="drawer-content">
    <!-- Language section -->
    <div class="drawer-section">
      <div class="section-label">{$strings.drawer?.language || 'Language'}</div>
      <div class="language-buttons">
        {#each availableLocales as item}
          <button
            class="lang-btn"
            class:active={$locale === item.code}
            onclick={() => handleLanguageSelect(item.code)}
          >
            {item.label}
          </button>
        {/each}
      </div>
    </div>

    <!-- Zoom section -->
    <div class="drawer-section">
      <div class="section-label">{$strings.drawer?.zoom || 'Zoom'}</div>
      <div class="zoom-row">
        <button
          class="zoom-btn"
          onclick={() => zoom.zoomOut()}
          disabled={$zoom <= ZOOM_MIN}
        >
          −
        </button>
        <span class="zoom-value">{Math.round($zoom * 100)}%</span>
        <button
          class="zoom-btn"
          onclick={() => zoom.zoomIn()}
          disabled={$zoom >= ZOOM_MAX}
        >
          +
        </button>
      </div>
    </div>

    <div class="drawer-section">
      <div class="section-label">{$strings.onboarding.panelTitle}</div>
      <div class="tour-card">
        <div class="tour-summary">{getTourSummary()}</div>
        <button class="tour-btn" onclick={restartTutorial}>
          {$strings.onboarding.buttons.restart}
        </button>
      </div>
    </div>

    <!-- Boards section -->
    <div class="drawer-section">
      <div class="section-label">{$strings.sidebar?.boards || 'Boards'}</div>
      <div class="cards-list">
        {#each $boards.items as board (board.id)}
          <button
            class="card-item"
            class:active={$boards.activeId === board.id}
            onclick={() => handleBoardSelect(board.id)}
          >
            <span class="card-text">{board.title}</span>
          </button>
        {/each}
        {#if $boards.items.length === 0}
          <div class="empty-cards">{$strings.sidebar?.empty || 'No boards yet'}</div>
        {/if}
      </div>
      <button class="new-session-btn" onclick={handleNewSession}>
        {$strings.sidebar?.newBoard || 'New board'}
      </button>
    </div>

    <!-- Cards list section -->
    <div class="drawer-section cards-section">
      <div class="section-label">{$strings.drawer?.cards || 'Cards'} ({cardList.length})</div>
      <div class="cards-list">
        {#each cardList as card (card.id)}
          <button class="card-item" onclick={() => handleCardClick(card.id)}>
            <span class="card-type-dot" style="background-color: {getCardTypeColor(card.type)}"></span>
            <span class="card-text">{card.text}</span>
          </button>
        {/each}
        {#if cardList.length === 0}
          <div class="empty-cards">{$strings.drawer?.noCards || 'No cards yet'}</div>
        {/if}
      </div>
    </div>
  </div>

  <!-- New session button at bottom -->
  {#if $hasSession}
    <div class="drawer-footer">
      <button class="new-session-btn" onclick={handleNewSession}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        {$strings.drawer?.newSession || 'New Session'}
      </button>
    </div>
  {/if}
</div>

<style>
  .drawer-scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 200;
    animation: fadeIn 0.2s ease;
  }

  .drawer {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: min(300px, 85vw);
    background: #fff;
    z-index: 210;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  }

  .drawer.open {
    transform: translateX(0);
  }

  .drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  }

  .drawer-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-dark);
  }

  .close-btn {
    width: 40px;
    height: 40px;
    border: none;
    background: transparent;
    color: var(--text-medium);
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s ease;
  }

  .close-btn:hover {
    background: rgba(0, 0, 0, 0.05);
  }

  .drawer-content {
    flex: 1;
    overflow-y: auto;
    padding: 12px 0;
  }

  .drawer-section {
    padding: 12px 20px;
  }

  .section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-light);
    font-weight: 600;
    margin-bottom: 10px;
  }

  .tour-card {
    border-radius: 14px;
    background: rgba(79, 70, 229, 0.06);
    border: 1px solid rgba(79, 70, 229, 0.12);
    padding: 12px;
  }

  .tour-summary {
    font-size: 13px;
    line-height: 1.5;
    color: var(--text-dark);
    margin-bottom: 10px;
  }

  .tour-btn {
    border: none;
    border-radius: 999px;
    padding: 10px 14px;
    background: #4f46e5;
    color: white;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
  }

  .language-buttons {
    display: flex;
    gap: 8px;
  }

  .lang-btn {
    flex: 1;
    padding: 10px 16px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    background: transparent;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-medium);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .lang-btn.active {
    background: rgba(149, 117, 205, 0.15);
    border-color: rgba(149, 117, 205, 0.3);
    color: #4a2e8a;
  }

  .lang-btn:hover:not(.active) {
    background: rgba(0, 0, 0, 0.04);
  }

  .zoom-row {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .zoom-btn {
    width: 44px;
    height: 44px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    background: #fff;
    font-size: 20px;
    font-weight: 600;
    color: var(--text-dark);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .zoom-btn:hover:not(:disabled) {
    background: rgba(0, 0, 0, 0.04);
  }

  .zoom-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .zoom-value {
    flex: 1;
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-dark);
  }

  .cards-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
  }

  .cards-list {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-height: 300px;
  }

  .card-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border: none;
    background: rgba(0, 0, 0, 0.02);
    border-radius: 8px;
    cursor: pointer;
    text-align: left;
    transition: background 0.2s ease;
  }

  .card-item:hover {
    background: rgba(0, 0, 0, 0.06);
  }

  .card-item.active {
    border: 1px solid rgba(149, 117, 205, 0.4);
    background: rgba(149, 117, 205, 0.12);
  }

  .card-type-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .card-text {
    flex: 1;
    font-size: 13px;
    color: var(--text-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .empty-cards {
    font-size: 13px;
    color: var(--text-light);
    text-align: center;
    padding: 20px;
  }

  .new-session-btn {
    margin-top: 10px;
    border: none;
    background: var(--question-purple);
    color: white;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 0.85em;
    cursor: pointer;
  }

  .drawer-footer {
    padding: 16px 20px;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
  }

  .new-session-btn {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px 16px;
    border: none;
    border-radius: 10px;
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .new-session-btn:hover {
    background: rgba(239, 68, 68, 0.18);
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
</style>
