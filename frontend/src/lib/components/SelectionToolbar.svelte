<script lang="ts">
  import { derived, get } from "svelte/store";
  import { cards } from "../stores/cards";
  import { selectedCardIds } from "../stores/selection";
  import { websocket } from "../stores/websocket";
  import { strings } from "../stores/i18n";
  import { trackSessionExported } from "../analytics";
  import { toPng } from "html-to-image";

  const selectionCount = derived(selectedCardIds, ($ids) => $ids.size);

  function getExportCards(onlyTodo: boolean) {
    let list = get(cards);
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
    downloadText(`clarify-board-${timestamp.toISOString().slice(0, 10)}.md`, header + lines.join("\n"));
    trackSessionExported(onlyTodo ? "markdown_todo" : "markdown_all");
  }

  async function exportImage() {
    const board = document.querySelector(".canvas-container") as HTMLElement | null;
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
</script>

<div class="selection-toolbar" class:active={$selectionCount > 0}>
  <div class="selection-count">
    {#if $selectionCount > 0}
      {$selectionCount} {$strings.toolbar?.selected || "selected"}
    {:else}
      {$strings.toolbar?.ready || "Canvas"}
    {/if}
  </div>
  <div class="selection-actions">
    <button class="toolbar-btn" onclick={() => adjustImportance(-0.05)}>
      {$strings.toolbar?.smaller || "Smaller"}
    </button>
    <button class="toolbar-btn" onclick={() => adjustImportance(0.05)}>
      {$strings.toolbar?.bigger || "Bigger"}
    </button>
    <button class="toolbar-btn" onclick={deleteSelected}>
      {$strings.toolbar?.delete || "Delete"}
    </button>
    <button class="toolbar-btn" onclick={() => exportList(false)}>
      {$strings.toolbar?.exportList || "Export list"}
    </button>
    <button class="toolbar-btn" onclick={() => exportList(true)}>
      {$strings.toolbar?.exportTodos || "Export todo"}
    </button>
    <button class="toolbar-btn" onclick={exportImage}>
      {$strings.toolbar?.exportImage || "Export image"}
    </button>
  </div>
</div>

<style>
  .selection-toolbar {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 10px 16px;
    border-radius: 999px;
    background: var(--bg-input);
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow-elevated);
    border: 1px solid var(--border-light);
    z-index: 130;
    opacity: 0.85;
    transition: opacity 0.2s ease, transform 0.2s ease;
  }

  .selection-toolbar.active {
    opacity: 1;
  }

  .selection-count {
    font-size: 0.85em;
    color: var(--text-medium);
    font-family: "Caveat", cursive;
  }

  .selection-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }

  .toolbar-btn {
    border: none;
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 0.8em;
    background: var(--accent-purple-subtle);
    color: var(--text-dark);
    cursor: pointer;
    transition: transform 0.15s ease, background 0.15s ease;
  }

  .toolbar-btn:hover {
    transform: translateY(-1px);
    background: var(--accent-purple-muted);
  }

  @media (max-width: 768px) {
    .selection-toolbar {
      flex-direction: column;
      gap: 8px;
      padding: 12px 14px;
      top: 12px;
      width: calc(100% - 24px);
      left: 12px;
      transform: none;
      border-radius: 18px;
    }

    .selection-actions {
      justify-content: center;
    }
  }
</style>
