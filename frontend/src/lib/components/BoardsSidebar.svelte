<script lang="ts">
  import { boards } from "../stores/boards";
  import { auth } from "../stores/auth";
  import { access, getAccessPaywallGate, summarizeAccessState } from "../stores/access";
  import { strings, availableLocales, locale, setLocale } from "../stores/i18n";
  import { zoom, ZOOM_MAX, ZOOM_MIN } from "../stores/zoom";
  import { helpOverlay } from "../stores/help";
  import { cards } from "../stores/cards";
  import { selectedCardIds } from "../stores/selection";
  import { websocket } from "../stores/websocket";
  import { derived, get } from "svelte/store";
  import { toPng } from "html-to-image";
  import { trackSessionExported } from "../analytics";
  import HelpOverlay from "./HelpOverlay.svelte";

  let authToken: string | null = null;
  let userName = $state("");
  let userInitials = $state("");
  let isCollapsed = $state(false);
  let isExportMenuOpen = $state(false);
  let openMenuId: string | null = $state(null);
  let isLegendCollapsed = $state(false);

  const selectionCount = derived(selectedCardIds, ($ids) => $ids.size);
  const accessSummary = derived(
    [access, strings, locale],
    ([$access, $strings, $locale]) => summarizeAccessState($access, $strings.access, $locale),
  );
  const newBoardGuidance = derived([access, strings], ([$access, $strings]) => {
    const gate = getAccessPaywallGate($access.snapshot);

    if (!gate.shouldShow) {
      return null;
    }

    return {
      body: $strings.access?.starterBlankBoardBody,
      action: $strings.access?.viewPlans || "View plans",
    };
  });

  $effect(() => {
    const unsubscribe = auth.subscribe((state) => {
      authToken = state.token;
      userName = state.user?.name || state.user?.email || "User";
      const parts = userName.trim().split(/\s+/);
      userInitials = parts.length >= 2
        ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
        : userName.slice(0, 2).toUpperCase();
    });
    return unsubscribe;
  });

  function selectBoard(boardId: string) {
    boards.setActiveBoard(boardId);
  }

  let menuOpenUp = $state(false);

  function toggleBoardMenu(e: Event, boardId: string) {
    e.stopPropagation();
    if (openMenuId === boardId) {
      openMenuId = null;
      return;
    }

    const button = e.currentTarget as HTMLElement;
    const rect = button.getBoundingClientRect();
    const menuHeight = 120;
    const spaceBelow = window.innerHeight - rect.bottom;
    menuOpenUp = spaceBelow < menuHeight;

    openMenuId = boardId;
  }

  function closeBoardMenu() {
    openMenuId = null;
  }

  async function handleDeleteBoard(e: Event, boardId: string) {
    e.stopPropagation();
    openMenuId = null;
    if (authToken && confirm("Delete this board?")) {
      await boards.deleteBoard(authToken, boardId);
    }
  }

  function handleExportFromMenu(e: Event, boardId: string) {
    e.stopPropagation();
    openMenuId = null;
    selectBoard(boardId);
    setTimeout(() => exportList(false), 100);
  }

  async function createBoard() {
    if (!authToken) return;
    await boards.createBoard(authToken);
  }

  function openUpgradePreview() {
    access.requestPaywallPrompt();
  }

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  // Export logic
  function getExportCards(onlyTodo: boolean) {
    const selected = get(selectedCardIds);
    let list = get(cards);
    if (selected.size > 0) {
      list = list.filter((card) => selected.has(card.id));
    }
    if (onlyTodo) {
      list = list.filter((card) => card.type === "todo");
    }
    return list;
  }

  function downloadText(filename: string, content: string) {
    const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  function exportList(onlyTodo: boolean) {
    const list = getExportCards(onlyTodo);
    if (list.length === 0) return;
    const timestamp = new Date();
    const header = `# Clarify Board Export\n\nGenerated: ${timestamp.toLocaleString()}\n\n`;
    const lines = list.map((card) => {
      if (card.type === "todo") {
        return `- [ ] ${card.text}`;
      }
      return `- (${card.type}) ${card.text}`;
    });
    downloadText(
      `clarify-board-${timestamp.toISOString().slice(0, 10)}.md`,
      header + lines.join("\n"),
    );
    trackSessionExported(onlyTodo ? "markdown_todo" : "markdown_all");
    isExportMenuOpen = false;
  }

  async function exportImage() {
    const board = document.querySelector(
      ".canvas-container",
    ) as HTMLElement | null;
    if (!board) return;
    try {
      const dataUrl = await toPng(board, { pixelRatio: 2 });
      const link = document.createElement("a");
      link.href = dataUrl;
      link.download = `clarify-board-${new Date().toISOString().slice(0, 10)}.png`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      trackSessionExported("image");
    } catch (error) {
      console.error("Export image failed", error);
    }
    isExportMenuOpen = false;
  }

  // Selection actions logic
  function adjustImportance(delta: number) {
    const selected = Array.from(get(selectedCardIds));
    if (selected.length === 0) return;
    const cardList = get(cards);
    for (const id of selected) {
      const card = cardList.find((item) => item.id === id);
      if (!card) continue;
      const next = Math.max(0, Math.min(1, card.importance + delta));
      cards.updateCard(id, { importance: next });
      websocket.sendCardUpdate(id, { importance: next });
    }
  }

  function deleteSelected() {
    const selected = Array.from(get(selectedCardIds));
    if (selected.length === 0) return;
    const cardList = get(cards);
    for (const id of selected) {
      const card = cardList.find((item) => item.id === id);
      if (!card || card.is_root) continue;
      websocket.sendCardDelete(id);
    }
    selectedCardIds.clear();
  }
</script>

<aside class="boards-sidebar" class:collapsed={isCollapsed}>
  <div class="sidebar-content">
    <!-- Header: logo + collapse -->
    <div class="sidebar-header">
      <div class="app-logo">Clarify Board</div>
      <button
        class="icon-btn"
        onclick={toggleSidebar}
        aria-label="Toggle Sidebar"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5" />
        </svg>
      </button>
    </div>

    <!-- New board row -->
    <button
      class="new-board-row"
      type="button"
      aria-describedby={$newBoardGuidance ? "new-board-guidance" : undefined}
      onclick={createBoard}
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <path d="M12 5v14" /><path d="M5 12h14" />
      </svg>
      {$strings.sidebar?.newBoard || "New board"}
    </button>
    {#if $newBoardGuidance}
      <div class="new-board-note" id="new-board-guidance">
        <p>{$newBoardGuidance.body}</p>
        <button
          class="access-link-btn"
          type="button"
          onclick={openUpgradePreview}
        >
          {$newBoardGuidance.action}
        </button>
      </div>
    {/if}

    <!-- Boards section -->
    <div class="section-label">{$strings.sidebar?.boards || "Boards"}</div>

    <div class="boards-list">
      {#if $boards.isLoading}
        <div class="boards-loading">
          {$strings.sidebar?.loading || "Loading..."}
        </div>
      {:else}
        {#each $boards.items as board (board.id)}
          <div
            class="board-item"
            class:active={$boards.activeId === board.id}
            class:demo={board.is_demo}
            role="button"
            tabindex="0"
            onclick={() => selectBoard(board.id)}
            onkeydown={(e) => e.key === 'Enter' && selectBoard(board.id)}
          >
            <span class="board-title">{board.title}</span>
            {#if !board.is_demo}
              <button
                class="board-dots"
                class:menu-open={openMenuId === board.id}
                onclick={(e) => toggleBoardMenu(e, board.id)}
                aria-label="Board actions"
              >
                <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor">
                  <circle cx="8" cy="3" r="1.2" /><circle cx="8" cy="8" r="1.2" /><circle cx="8" cy="13" r="1.2" />
                </svg>
              </button>
              {#if openMenuId === board.id}
                <div class="context-menu" class:open-up={menuOpenUp}>
                  <button
                    class="menu-item"
                    onclick={(e) => handleExportFromMenu(e, board.id)}
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
                    </svg>
                    {$strings.sidebar?.export || "Export"}
                  </button>
                  <div class="menu-divider"></div>
                  <button
                    class="menu-item danger"
                    onclick={(e) => handleDeleteBoard(e, board.id)}
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    </svg>
                    {$strings.sidebar?.delete || "Delete"}
                  </button>
                </div>
                <div
                  class="board-menu-scrim"
                  onclick={closeBoardMenu}
                ></div>
              {/if}
            {/if}
          </div>
        {/each}
        {#if $boards.items.length === 0}
          <div class="boards-empty">
            {$strings.sidebar?.empty || "No boards yet"}
          </div>
        {/if}
      {/if}
    </div>

    <!-- Selection Actions Section -->
    {#if $selectionCount > 0}
      <div class="selection-section">
        <div class="section-label">
          {$selectionCount}
          {$strings.toolbar?.selected || "selected"}
        </div>
        <div class="selection-grid">
          <button
            class="tool-btn"
            onclick={() => adjustImportance(-0.05)}
            title={$strings.toolbar?.smaller}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12H4" /></svg>
          </button>
          <button
            class="tool-btn"
            onclick={() => adjustImportance(0.05)}
            title={$strings.toolbar?.bigger}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14" /></svg>
          </button>
          <button
            class="tool-btn delete"
            onclick={deleteSelected}
            title={$strings.toolbar?.delete}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>
          </button>
        </div>
      </div>
    {/if}

    <!-- Utilities row -->
    <div class="utilities-section">
      <!-- Language switcher -->
      <div class="util-group">
        {#each availableLocales as item}
          <button
            class="util-btn"
            class:active={$locale === item.code}
            onclick={() => setLocale(item.code)}
          >
            {item.code.toUpperCase()}
          </button>
        {/each}
      </div>

      <div class="util-sep"></div>

      <!-- Zoom -->
      <div class="util-group">
        <button
          class="util-btn"
          onclick={() => zoom.zoomOut()}
          disabled={$zoom <= ZOOM_MIN}
          title={$strings.zoom.outTitle}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12" /></svg>
        </button>
        <button
          class="util-btn"
          onclick={() => zoom.zoomIn()}
          disabled={$zoom >= ZOOM_MAX}
          title={$strings.zoom.inTitle}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
        </button>
      </div>

      <div class="util-sep"></div>

      <!-- Export -->
      <div class="export-container">
        <button
          class="util-single"
          onclick={() => (isExportMenuOpen = !isExportMenuOpen)}
          title={$strings.toolbar?.exportList}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" y1="15" x2="12" y2="3" />
          </svg>
        </button>
        {#if isExportMenuOpen}
          <div class="export-dropdown">
            <button class="dropdown-item" onclick={() => exportList(false)}>
              {$strings.toolbar?.exportList}
            </button>
            <button class="dropdown-item" onclick={() => exportList(true)}>
              {$strings.toolbar?.exportTodos}
            </button>
            <button class="dropdown-item" onclick={exportImage}>
              {$strings.toolbar?.exportImage}
            </button>
          </div>
          <div
            class="menu-scrim"
            onclick={() => (isExportMenuOpen = false)}
          ></div>
        {/if}
      </div>

      <!-- Help -->
      <div class="help-wrapper">
        <button
          class="util-single"
          onclick={() => helpOverlay.toggle()}
          title={$strings.help.buttonLabel}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
        </button>
        <HelpOverlay />
      </div>
    </div>

    <!-- Card legend -->
    <div class="legend-section">
      <div
        class="legend-header"
        role="button"
        tabindex="0"
        onclick={() => (isLegendCollapsed = !isLegendCollapsed)}
        onkeydown={(e) => e.key === 'Enter' && (isLegendCollapsed = !isLegendCollapsed)}
      >
        <span class="legend-title">{$strings.canvas.legendTitle}</span>
        <button
          class="legend-toggle"
          class:collapsed={isLegendCollapsed}
          aria-label="Toggle legend"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M6 9l6 6 6-6" />
          </svg>
        </button>
      </div>
      <div class="legend-grid" class:hidden={isLegendCollapsed}>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--question-purple);"></span>
          <span class="legend-label">{$strings.canvas.legend.question}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--fact-blue);"></span>
          <span class="legend-label">{$strings.canvas.legend.fact}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--pain-red);"></span>
          <span class="legend-label">{$strings.canvas.legend.pain}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--resource-green);"></span>
          <span class="legend-label">{$strings.canvas.legend.resource}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--hypothesis-amber);"></span>
          <span class="legend-label">{$strings.canvas.legend.hypothesis}</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--todo-teal);"></span>
          <span class="legend-label">{$strings.canvas.legend.todo}</span>
        </div>
      </div>
    </div>

    <!-- Footer: avatar + name + plan + logout -->
    <div class="sidebar-footer">
      <div class="user-avatar">{userInitials}</div>
      <div class="user-meta">
        <div class="user-name">{userName}</div>
        <button
          class="user-plan"
          type="button"
          onclick={openUpgradePreview}
        >
          {$accessSummary.title}
        </button>
      </div>
      <button class="logout-btn" onclick={() => auth.logout()} title={$strings.sidebar?.logout || "Logout"}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><polyline points="16 17 21 12 16 7" /><line x1="21" y1="12" x2="9" y2="12" />
        </svg>
      </button>
    </div>
  </div>
</aside>

<!-- Collapsed toggle button (only shown when collapsed) -->
{#if isCollapsed}
  <button
    class="collapsed-toggle"
    onclick={toggleSidebar}
    aria-label="Open Sidebar"
  >
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13 17l5-5-5-5M6 17l5-5-5-5" />
    </svg>
  </button>
{/if}

<style>
  /* ─── Sidebar shell ─── */
  .boards-sidebar {
    width: 260px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border-light);
    box-shadow: 8px 0 24px rgba(0, 0, 0, 0.08);
    z-index: 120;
    transition:
      width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      padding 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .boards-sidebar.collapsed {
    width: 0;
    border-right: none;
  }

  .sidebar-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    opacity: 1;
    transition: opacity 0.2s ease;
    width: 260px;
  }

  .collapsed .sidebar-content {
    opacity: 0;
    pointer-events: none;
  }

  /* ─── Collapsed toggle (outside sidebar) ─── */
  .collapsed-toggle {
    position: fixed;
    left: 8px;
    top: 14px;
    width: 30px;
    height: 30px;
    border: none;
    background: var(--bg-input);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 130;
    box-shadow: var(--shadow-soft);
    color: var(--text-light);
    transition: background 0.15s, color 0.15s;
  }

  .collapsed-toggle:hover {
    background: var(--bg-surface);
    color: var(--text-medium);
  }

  /* ─── Header ─── */
  .sidebar-header {
    padding: 14px 14px 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .app-logo {
    font-family: "Caveat", cursive;
    font-size: 21px;
    font-weight: 500;
    color: var(--text-dark);
    flex: 1;
    padding-left: 2px;
    line-height: 1;
  }

  .icon-btn {
    width: 30px;
    height: 30px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-light);
    transition: background 0.15s, color 0.15s;
    flex-shrink: 0;
  }

  .icon-btn:hover {
    background: var(--bg-surface-active);
    color: var(--text-medium);
  }

  /* ─── New board row ─── */
  .new-board-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 14px;
    margin: 0 8px 4px;
    border-radius: 8px;
    cursor: pointer;
    border: none;
    background: transparent;
    font-family: inherit;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-medium);
    transition: background 0.12s, color 0.12s;
    width: calc(100% - 16px);
    text-align: left;
  }

  .new-board-row:hover {
    background: var(--accent-purple-subtle);
    color: var(--accent-purple);
  }

  .new-board-note {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    padding: 10px 12px;
    margin: 0 8px 4px;
    border-radius: 10px;
    background: var(--accent-purple-subtle);
    border: 1px solid var(--accent-purple-muted);
  }

  .new-board-note p {
    margin: 0;
    font-size: 0.79em;
    line-height: 1.45;
    color: var(--text-medium);
  }

  .access-link-btn {
    border: none;
    padding: 0;
    background: transparent;
    color: var(--accent-purple);
    font-size: 0.79em;
    font-weight: 700;
    cursor: pointer;
  }

  .access-link-btn:hover {
    color: var(--text-dark);
  }

  /* ─── Section label ─── */
  .section-label {
    padding: 10px 16px 6px;
    font-size: 10px;
    font-weight: 700;
    color: var(--text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  /* ─── Boards list ─── */
  .boards-list {
    flex: 1;
    overflow-y: auto;
    padding: 0 8px;
    min-height: 0;
  }

  .boards-list::-webkit-scrollbar {
    width: 3px;
  }
  .boards-list::-webkit-scrollbar-track {
    background: transparent;
  }
  .boards-list::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 2px;
  }

  .boards-loading,
  .boards-empty {
    padding: 12px 10px;
    font-size: 12px;
    color: var(--text-subtle);
  }

  .board-item {
    display: flex;
    align-items: center;
    padding: 8px 10px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.1s;
    position: relative;
  }

  .board-item:hover {
    background: var(--bg-surface-hover);
  }

  .board-item.active {
    background: var(--accent-purple-subtle);
  }

  .board-item.active .board-title {
    font-weight: 600;
  }

  .board-item.demo {
    border: 1.5px dashed var(--accent-purple-muted);
    background: var(--accent-purple-subtle);
  }

  .board-item.demo .board-title {
    font-style: italic;
    color: var(--text-medium);
  }

  .board-title {
    flex: 1;
    font-size: 13px;
    color: var(--text-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.4;
  }

  /* ─── Three dots ─── */
  .board-dots {
    width: 26px;
    height: 26px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-light);
    opacity: 0;
    transition: opacity 0.1s, background 0.1s;
    flex-shrink: 0;
    position: relative;
  }

  .board-item:hover .board-dots {
    opacity: 1;
  }

  .board-dots:hover {
    background: var(--bg-surface-active);
  }

  .board-dots.menu-open {
    opacity: 1;
    background: var(--bg-surface-active);
  }

  /* ─── Context menu ─── */
  .context-menu {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 4px;
    background: var(--bg-menu);
    border-radius: 10px;
    box-shadow: var(--shadow-elevated), 0 0 0 1px var(--border-light);
    padding: 4px;
    z-index: 150;
    min-width: 170px;
  }

  .context-menu.open-up {
    top: auto;
    bottom: 100%;
    margin-top: 0;
    margin-bottom: 4px;
  }

  .menu-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 13px;
    color: var(--text-dark);
    transition: background 0.1s;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
    font-family: inherit;
  }

  .menu-item:hover {
    background: var(--bg-surface-hover);
  }

  .menu-item.danger {
    color: var(--danger);
  }

  .menu-item.danger:hover {
    background: var(--danger-subtle);
  }

  .menu-divider {
    height: 1px;
    background: var(--border-light);
    margin: 3px 8px;
  }

  .board-menu-scrim {
    position: fixed;
    inset: 0;
    z-index: 140;
    background: transparent;
  }

  /* ─── Selection section ─── */
  .selection-section {
    border-top: 1px solid var(--border-light);
    padding: 10px 14px;
  }

  .selection-grid {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 6px;
  }

  .tool-btn {
    width: 30px;
    height: 28px;
    border: none;
    background: var(--bg-surface-hover);
    border-radius: 7px;
    border: 1px solid var(--border-light);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-medium);
    transition: background 0.12s, color 0.12s;
  }

  .tool-btn:hover {
    background: var(--bg-surface-active);
    color: var(--text-dark);
  }

  .tool-btn.delete:hover {
    color: var(--danger);
    background: var(--danger-subtle);
  }

  /* ─── Utilities row ─── */
  .utilities-section {
    border-top: 1px solid var(--border-light);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: nowrap;
  }

  .util-group {
    display: flex;
    background: var(--bg-surface-hover);
    border-radius: 7px;
    border: 1px solid var(--border-light);
    overflow: hidden;
  }

  .util-btn {
    width: 30px;
    height: 28px;
    border: none;
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-medium);
    font-family: inherit;
    font-size: 11px;
    font-weight: 600;
    transition: background 0.12s, color 0.12s;
  }

  .util-btn:hover {
    background: var(--bg-surface-active);
  }

  .util-btn.active {
    background: var(--bg-surface);
    color: var(--accent-purple);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  }

  .util-btn:disabled {
    opacity: 0.35;
    cursor: default;
  }

  .util-sep {
    width: 1px;
    height: 16px;
    background: var(--border-light);
    align-self: center;
    flex-shrink: 0;
  }

  .util-single {
    width: 30px;
    height: 28px;
    border: 1px solid var(--border-light);
    background: var(--bg-surface-hover);
    border-radius: 7px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-medium);
    transition: background 0.12s, color 0.12s;
  }

  .util-single:hover {
    background: var(--bg-surface-active);
    color: var(--text-dark);
  }

  .export-container {
    position: relative;
    z-index: 140;
  }

  .export-dropdown {
    position: absolute;
    bottom: 36px;
    left: 0;
    background: var(--bg-menu);
    border-radius: 10px;
    box-shadow: var(--shadow-elevated), 0 0 0 1px var(--border-light);
    padding: 4px;
    display: flex;
    flex-direction: column;
    min-width: 160px;
    z-index: 150;
    animation: slideUp 0.15s ease-out;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(6px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .dropdown-item {
    border: none;
    background: transparent;
    text-align: left;
    padding: 8px 12px;
    border-radius: 7px;
    font-size: 13px;
    color: var(--text-dark);
    cursor: pointer;
    transition: background 0.1s;
    font-family: inherit;
  }

  .dropdown-item:hover {
    background: var(--accent-purple-subtle);
    color: var(--accent-purple);
  }

  .menu-scrim {
    position: fixed;
    inset: 0;
    z-index: 135;
    background: transparent;
  }

  .help-wrapper {
    position: relative;
  }

  /* ─── Card legend ─── */
  .legend-section {
    border-top: 1px solid var(--border-light);
    padding: 8px 14px;
  }

  .legend-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    padding: 2px 0;
  }

  .legend-title {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  .legend-toggle {
    width: 20px;
    height: 20px;
    border: none;
    background: transparent;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-subtle);
    transition: transform 0.2s;
    border-radius: 4px;
    pointer-events: none;
  }

  .legend-toggle:hover {
    color: var(--text-light);
  }

  .legend-toggle.collapsed {
    transform: rotate(-90deg);
  }

  .legend-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 12px;
    margin-top: 8px;
    overflow: hidden;
    transition: max-height 0.25s ease, opacity 0.2s ease, margin 0.25s ease;
    max-height: 120px;
    opacity: 1;
  }

  .legend-grid.hidden {
    max-height: 0;
    opacity: 0;
    margin-top: 0;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 2px 0;
  }

  .legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .legend-label {
    font-size: 11px;
    color: var(--text-medium);
    line-height: 1.2;
  }

  /* ─── Footer ─── */
  .sidebar-footer {
    border-top: 1px solid var(--border-light);
    padding: 10px 14px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #9575cd, #7e57c2);
    color: white;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    letter-spacing: 0.3px;
  }

  .user-meta {
    flex: 1;
    min-width: 0;
  }

  .user-name {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-dark);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .user-plan {
    font-size: 10px;
    color: var(--text-subtle);
    margin-top: 1px;
    border: none;
    background: none;
    padding: 0;
    cursor: pointer;
    text-align: left;
    font-family: inherit;
    transition: color 0.15s;
  }

  .user-plan:hover {
    color: var(--accent-purple);
  }

  .logout-btn {
    width: 30px;
    height: 30px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-subtle);
    transition: background 0.15s, color 0.15s;
    flex-shrink: 0;
  }

  .logout-btn:hover {
    background: var(--bg-surface-active);
    color: var(--text-medium);
  }

  @media (max-width: 900px) {
    .boards-sidebar {
      display: none;
    }
    .collapsed-toggle {
      display: none;
    }
  }
</style>
