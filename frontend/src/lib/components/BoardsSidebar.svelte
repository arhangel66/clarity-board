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
  let isCollapsed = $state(false);
  let isExportMenuOpen = $state(false);
  let openMenuId: string | null = $state(null);

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

    // Check if menu would overflow bottom of viewport
    const button = e.currentTarget as HTMLElement;
    const rect = button.getBoundingClientRect();
    const menuHeight = 50; // approximate menu height
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
    const header = `# Fact Cards Export\n\nGenerated: ${timestamp.toLocaleString()}\n\n`;
    const lines = list.map((card) => {
      if (card.type === "todo") {
        return `- [ ] ${card.text}`;
      }
      return `- (${card.type}) ${card.text}`;
    });
    downloadText(
      `fact-cards-${timestamp.toISOString().slice(0, 10)}.md`,
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
      link.download = `fact-cards-${new Date().toISOString().slice(0, 10)}.png`;
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
  <button
    class="toggle-btn"
    onclick={toggleSidebar}
    aria-label="Toggle Sidebar"
  >
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
    >
      {#if isCollapsed}
        <path d="M13 17l5-5-5-5M6 17l5-5-5-5" />
      {:else}
        <path d="M11 17l-5-5 5-5M18 17l-5-5 5-5" />
      {/if}
    </svg>
  </button>

  <div class="sidebar-content">
    <div class="sidebar-header">
      <div class="app-name">Fact Cards</div>
      <div class="new-board-stack">
        <button
          class="new-board-btn"
          type="button"
          aria-describedby={$newBoardGuidance ? "new-board-guidance" : undefined}
          onclick={createBoard}
        >
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
      </div>
    </div>

    <section
      class="access-card"
      class:paid={$accessSummary.tone === "paid"}
      class:warning={$accessSummary.tone === "warning"}
      class:error={$accessSummary.tone === "error"}
    >
      <div class="access-top">
        <div class="access-copy">
          <div class="access-kicker">{$strings.access?.kicker || "Access"}</div>
          <div class="access-title">{$accessSummary.title}</div>
          <p class="access-detail">{$accessSummary.detail}</p>
        </div>
        {#if $accessSummary.total && $accessSummary.remaining !== null}
          <div
            class="access-meter"
            aria-label={$strings.access?.starterTitle || "Starter access"}
          >
            {#each Array.from({ length: $accessSummary.total }) as _, index}
              <span
                class="access-meter-dot"
                class:available={index < $accessSummary.remaining}
              ></span>
            {/each}
          </div>
        {/if}
      </div>
      {#if $accessSummary.note}
        <p class="access-note">{$accessSummary.note}</p>
      {/if}
    </section>

    <div class="boards-section">
      <div class="section-title">{$strings.sidebar?.boards || "Boards"}</div>
      {#if $boards.isLoading}
        <div class="boards-loading">
          {$strings.sidebar?.loading || "Loading..."}
        </div>
      {:else}
        <div class="boards-list">
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
              <div class="board-content">
                <div class="board-title">
                  {board.title}
                </div>
                {#if !board.is_demo}
                  <div class="board-meta">
                    {new Date(board.updated_at).toLocaleDateString()}
                  </div>
                {/if}
              </div>
              {#if !board.is_demo}
                <div class="board-actions">
                  <button
                    class="more-btn"
                    onclick={(e) => toggleBoardMenu(e, board.id)}
                    aria-label="Board actions"
                  >
                    ⋮
                  </button>
                  {#if openMenuId === board.id}
                    <div class="board-dropdown" class:open-up={menuOpenUp}>
                      <button
                        class="board-menu-item delete"
                        onclick={(e) => handleDeleteBoard(e, board.id)}
                      >
                        Delete
                      </button>
                    </div>
                    <div
                      class="board-menu-scrim"
                      onclick={closeBoardMenu}
                    ></div>
                  {/if}
                </div>
              {/if}
            </div>
          {/each}
          {#if $boards.items.length === 0}
            <div class="boards-empty">
              {$strings.sidebar?.empty || "No boards yet"}
            </div>
          {/if}
        </div>
      {/if}
    </div>

    <!-- Selection Actions Section -->
    {#if $selectionCount > 0}
      <div class="selection-section">
        <div class="section-title">
          {$selectionCount}
          {$strings.toolbar?.selected || "selected"}
        </div>
        <div class="selection-grid">
          <button
            class="tool-btn"
            onclick={() => adjustImportance(-0.05)}
            title={$strings.toolbar?.smaller}
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"><path d="M20 12H4" /></svg
            >
          </button>
          <button
            class="tool-btn"
            onclick={() => adjustImportance(0.05)}
            title={$strings.toolbar?.bigger}
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"><path d="M12 5v14M5 12h14" /></svg
            >
          </button>
          <button
            class="tool-btn delete"
            onclick={deleteSelected}
            title={$strings.toolbar?.delete}
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              ><path
                d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
              /></svg
            >
          </button>
        </div>
      </div>
    {/if}

    <div class="tools-section">
      <div class="section-title">{$strings.drawer?.title || "Tools"}</div>
      <div class="tools-grid">
        <!-- Export Menu -->
        <div class="export-container">
          <button
            class="tool-btn"
            onclick={() => (isExportMenuOpen = !isExportMenuOpen)}
            title={$strings.toolbar?.exportList}
          >
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"
              />
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

        <!-- Language -->
        <div class="tool-group">
          {#each availableLocales as item}
            <button
              class="mini-btn"
              class:active={$locale === item.code}
              onclick={() => setLocale(item.code)}
            >
              {item.code.toUpperCase()}
            </button>
          {/each}
        </div>

        <!-- Zoom -->
        <div class="tool-group">
          <button
            class="mini-btn"
            onclick={() => zoom.zoomIn()}
            disabled={$zoom >= ZOOM_MAX}
            title={$strings.zoom.inTitle}
          >
            +
          </button>
          <button
            class="mini-btn"
            onclick={() => zoom.zoomOut()}
            disabled={$zoom <= ZOOM_MIN}
            title={$strings.zoom.outTitle}
          >
            −
          </button>
        </div>

        <!-- Help -->
        <div class="help-wrapper">
          <button
            class="tool-btn"
            onclick={() => helpOverlay.toggle()}
            title={$strings.help.buttonLabel}
          >
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
          </button>
          <HelpOverlay />
        </div>
      </div>
    </div>

    <div class="legend-section">
      <div class="section-title">{$strings.canvas.legendTitle}</div>
      <div class="legend-grid">
        <div class="legend-item">
          <div
            class="legend-color"
            style="background: var(--question-purple);"
          ></div>
          <span class="legend-label">{$strings.canvas.legend.question}</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: var(--fact-blue);"></div>
          <span class="legend-label">{$strings.canvas.legend.fact}</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: var(--pain-red);"></div>
          <span class="legend-label">{$strings.canvas.legend.pain}</span>
        </div>
        <div class="legend-item">
          <div
            class="legend-color"
            style="background: var(--resource-green);"
          ></div>
          <span class="legend-label">{$strings.canvas.legend.resource}</span>
        </div>
        <div class="legend-item">
          <div
            class="legend-color"
            style="background: var(--hypothesis-amber);"
          ></div>
          <span class="legend-label">{$strings.canvas.legend.hypothesis}</span>
        </div>
        <div class="legend-item">
          <div class="legend-color" style="background: var(--todo-teal);"></div>
          <span class="legend-label">{$strings.canvas.legend.todo}</span>
        </div>
      </div>
    </div>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-name">{userName}</div>
        <button class="logout-btn" onclick={() => auth.logout()}>
          {$strings.sidebar?.logout || "Logout"}
        </button>
      </div>
    </div>
  </div>
</aside>

<style>
  .boards-sidebar {
    width: 280px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(180deg, #f9f5ef 0%, #f0e7da 100%);
    border-right: 1px solid rgba(0, 0, 0, 0.05);
    padding: 20px 16px;
    box-shadow: 8px 0 24px rgba(0, 0, 0, 0.08);
    z-index: 120;
    transition:
      width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
      padding 0.3s ease;
    position: relative;
    overflow: visible;
  }

  .boards-sidebar.collapsed {
    width: 0;
    padding: 20px 0;
    border-right: none;
  }

  .sidebar-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    opacity: 1;
    transition: opacity 0.2s ease;
    width: 248px; /* 280 - 16*2 */
  }

  .collapsed .sidebar-content {
    opacity: 0;
    pointer-events: none;
  }

  .toggle-btn {
    position: absolute;
    right: -16px;
    top: 20px;
    width: 32px;
    height: 32px;
    background: white;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 130;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    color: var(--text-medium);
    transition:
      color 0.2s ease,
      transform 0.2s ease;
  }

  .toggle-btn:hover {
    color: var(--question-purple);
    transform: scale(1.05);
  }

  .sidebar-header {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 14px;
  }

  .new-board-stack {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .access-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 12px 14px;
    margin-bottom: 14px;
    border-radius: 16px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.9),
      rgba(247, 236, 214, 0.78)
    );
    border: 1px solid rgba(145, 110, 63, 0.14);
    box-shadow: 0 6px 18px rgba(116, 84, 44, 0.06);
  }

  .access-card.paid {
    background: linear-gradient(
      135deg,
      rgba(238, 247, 239, 0.96),
      rgba(219, 239, 223, 0.92)
    );
    border-color: rgba(62, 117, 74, 0.16);
  }

  .access-card.warning {
    background: linear-gradient(
      135deg,
      rgba(255, 243, 228, 0.97),
      rgba(255, 230, 210, 0.95)
    );
    border-color: rgba(184, 106, 43, 0.18);
  }

  .access-card.error {
    background: linear-gradient(
      135deg,
      rgba(245, 242, 239, 0.96),
      rgba(235, 229, 223, 0.92)
    );
    border-color: rgba(107, 90, 77, 0.14);
  }

  .access-kicker {
    font-size: 0.68em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(109, 79, 42, 0.72);
  }

  .access-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
  }

  .access-copy {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }

  .access-title {
    font-size: 0.98em;
    font-weight: 700;
    color: var(--text-dark);
  }

  .access-detail,
  .access-note {
    margin: 0;
    font-size: 0.8em;
    line-height: 1.45;
    color: var(--text-medium);
  }

  .access-note {
    color: rgba(98, 72, 40, 0.82);
  }

  .access-meter {
    display: flex;
    gap: 6px;
    margin-top: 2px;
    padding-top: 4px;
  }

  .access-meter-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: rgba(109, 79, 42, 0.14);
    overflow: hidden;
  }

  .access-meter-dot.available {
    background: linear-gradient(90deg, #d5a65b 0%, #f0c977 100%);
  }

  .app-name {
    font-family: "Caveat", cursive;
    font-size: 1.8em;
    color: var(--text-dark);
  }

  .new-board-note {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    padding: 10px 12px;
    border-radius: 14px;
    background: rgba(255, 244, 231, 0.96);
    border: 1px solid rgba(184, 106, 43, 0.16);
  }

  .new-board-note p {
    margin: 0;
    font-size: 0.79em;
    line-height: 1.45;
    color: rgba(104, 70, 31, 0.92);
  }

  .new-board-btn {
    border: none;
    padding: 10px 12px;
    border-radius: 14px;
    background: var(--question-purple);
    color: white;
    font-size: 0.9em;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 6px 16px rgba(149, 117, 205, 0.3);
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
  }

  .new-board-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(149, 117, 205, 0.4);
  }

  .access-link-btn {
    border: none;
    padding: 0;
    background: transparent;
    color: #8d5a18;
    font-size: 0.79em;
    font-weight: 700;
    cursor: pointer;
  }

  .access-link-btn:hover {
    color: #6e4310;
  }

  .boards-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 0;
  }

  .section-title {
    font-size: 0.7em;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-light);
    margin-bottom: 4px;
  }

  .boards-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
    padding-right: 4px;
  }

  .board-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: none;
    text-align: left;
    padding: 12px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
  }

  .board-item:hover {
    background: rgba(255, 255, 255, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }

  .board-item.active {
    background: white;
    border: 1px solid rgba(149, 117, 205, 0.3);
    box-shadow: 0 4px 20px rgba(149, 117, 205, 0.15);
  }

  .board-item.demo {
    border: 1.5px dashed rgba(149, 117, 205, 0.35);
    background: rgba(243, 237, 255, 0.5);
  }

  .board-item.demo .board-title {
    font-style: italic;
    color: var(--text-medium);
  }

  .board-content {
    flex: 1;
    min-width: 0;
  }

  .board-title {
    font-size: 0.95em;
    color: var(--text-dark);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .board-meta {
    font-size: 0.75em;
    color: var(--text-light);
    margin-top: 4px;
  }

  .board-actions {
    position: relative;
    opacity: 0;
    transition: opacity 0.15s ease;
  }

  .board-item:hover .board-actions {
    opacity: 1;
  }

  .more-btn {
    background: none;
    border: none;
    padding: 4px 8px;
    cursor: pointer;
    font-size: 16px;
    color: var(--text-medium);
    border-radius: 6px;
    transition: background 0.15s ease;
  }

  .more-btn:hover {
    background: rgba(0, 0, 0, 0.06);
  }

  .board-dropdown {
    position: absolute;
    right: 0;
    top: 100%;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    min-width: 120px;
    z-index: 150;
    padding: 4px;
  }

  .board-dropdown.open-up {
    top: auto;
    bottom: 100%;
  }

  .board-menu-item {
    display: block;
    width: 100%;
    padding: 8px 12px;
    text-align: left;
    border: none;
    background: none;
    cursor: pointer;
    font-size: 0.85em;
    border-radius: 6px;
    transition: background 0.15s ease;
  }

  .board-menu-item.delete {
    color: #ef4444;
  }

  .board-menu-item:hover {
    background: rgba(0, 0, 0, 0.05);
  }

  .board-menu-scrim {
    position: fixed;
    inset: 0;
    z-index: 140;
    background: transparent;
  }

  .selection-section,
  .tools-section {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
  }

  .selection-grid,
  .tools-grid {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
    flex-wrap: wrap;
  }

  .tool-group {
    display: flex;
    background: rgba(255, 255, 255, 0.5);
    padding: 2px;
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0.04);
  }

  .tool-btn,
  .mini-btn {
    border: none;
    background: white;
    color: var(--text-dark);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  }

  .tool-btn {
    width: 36px;
    height: 36px;
    border-radius: 10px;
  }

  .mini-btn {
    padding: 4px 8px;
    min-width: 32px;
    height: 28px;
    font-size: 0.75em;
    font-weight: 700;
    border-radius: 8px;
    background: transparent;
    box-shadow: none;
  }

  .mini-btn.active {
    background: white;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    color: var(--question-purple);
  }

  .tool-btn:hover,
  .mini-btn:hover:not(.active) {
    background: white;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .tool-btn.delete:hover {
    color: #e53935;
    background: #ffebee;
  }

  .help-wrapper {
    position: relative;
  }

  .export-container {
    position: relative;
    z-index: 140;
  }

  .export-dropdown {
    position: absolute;
    bottom: 44px;
    left: 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(0, 0, 0, 0.08);
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 160px;
    z-index: 150;
    animation: slideUp 0.2s ease-out;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(10px);
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
    padding: 10px 12px;
    border-radius: 8px;
    font-size: 0.85em;
    color: var(--text-dark);
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .dropdown-item:hover {
    background: rgba(149, 117, 205, 0.1);
    color: var(--question-purple);
  }

  .menu-scrim {
    position: fixed;
    inset: 0;
    z-index: 135;
    background: transparent;
  }

  .sidebar-footer {
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
  }

  .legend-section {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
  }

  .legend-grid {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .legend-color {
    width: 14px;
    height: 14px;
    border-radius: 4px;
    flex-shrink: 0;
  }

  .legend-label {
    font-size: 0.85em;
    color: var(--text-medium);
  }

  .user-info {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .user-name {
    font-size: 0.9em;
    color: var(--text-dark);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .logout-btn {
    border: none;
    background: transparent;
    color: var(--text-light);
    cursor: pointer;
    font-size: 0.8em;
    padding: 4px 8px;
    border-radius: 6px;
    transition: all 0.2s ease;
  }

  .logout-btn:hover {
    background: rgba(0, 0, 0, 0.04);
    color: var(--text-dark);
  }

  @media (max-width: 900px) {
    .boards-sidebar {
      display: none;
    }
  }
</style>
