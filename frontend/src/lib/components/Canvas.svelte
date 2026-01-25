<script lang="ts">
  import { onMount } from "svelte";
  import { cards } from "../stores/cards";
  import { selectedCardIds } from "../stores/selection";
  import { zoom } from "../stores/zoom";
  import { strings } from "../stores/i18n";
  import { websocket } from "../stores/websocket";
  import Card from "./Card.svelte";
  import Connections from "./Connections.svelte";
  import { get } from "svelte/store";

  let cardsContainer: HTMLDivElement | null = null;
  let suppressClick = $state(false);
  let isLassoing = $state(false);
  let lassoAdditive = false;
  let lassoStartX = 0;
  let lassoStartY = 0;
  let lassoRender = $state({ left: 0, top: 0, width: 0, height: 0 });

  function handleCanvasClick(e: MouseEvent) {
    // Deselect if clicked on cards-container (not on a card)
    const target = e.target as HTMLElement;
    if (target.classList.contains("cards-container")) {
      if (suppressClick) {
        suppressClick = false;
        return;
      }
      selectedCardIds.clear();
    }
  }

  function adjustSelectedImportance(delta: number) {
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

  function deleteSelectedCards() {
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

  function shouldIgnoreKey(event: KeyboardEvent): boolean {
    const target = event.target as HTMLElement | null;
    if (!target) return false;
    return (
      target.tagName === "INPUT" ||
      target.tagName === "TEXTAREA" ||
      target.isContentEditable
    );
  }

  onMount(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (shouldIgnoreKey(event)) return;
      if (event.key === "=" || event.key === "+") {
        event.preventDefault();
        adjustSelectedImportance(0.05);
      }
      if (event.key === "-" || event.key === "_") {
        event.preventDefault();
        adjustSelectedImportance(-0.05);
      }
      if (event.key === "Escape") {
        selectedCardIds.clear();
      }
      if (
        (event.key === "Backspace" || event.key === "Delete") &&
        get(selectedCardIds).size > 0
      ) {
        event.preventDefault();
        deleteSelectedCards();
      }
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "a") {
        event.preventDefault();
        const allIds = get(cards).map((card) => card.id);
        selectedCardIds.set(allIds);
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  function updateLassoRender(clientX: number, clientY: number) {
    if (!cardsContainer) return;
    const containerRect = cardsContainer.getBoundingClientRect();
    const minX = Math.min(lassoStartX, clientX);
    const minY = Math.min(lassoStartY, clientY);
    const maxX = Math.max(lassoStartX, clientX);
    const maxY = Math.max(lassoStartY, clientY);
    lassoRender = {
      left: minX - containerRect.left,
      top: minY - containerRect.top,
      width: maxX - minX,
      height: maxY - minY,
    };
  }

  function handleLassoStart(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.classList.contains("cards-container")) return;
    suppressClick = true;
    lassoAdditive = event.shiftKey || event.metaKey || event.ctrlKey;
    isLassoing = true;
    lassoStartX = event.clientX;
    lassoStartY = event.clientY;
    updateLassoRender(event.clientX, event.clientY);
    document.addEventListener("mousemove", handleLassoMove);
    document.addEventListener("mouseup", handleLassoEnd);
    event.preventDefault();
  }

  function handleLassoMove(event: MouseEvent) {
    if (!isLassoing) return;
    updateLassoRender(event.clientX, event.clientY);
  }

  function handleLassoEnd(event: MouseEvent) {
    if (!isLassoing || !cardsContainer) return;
    document.removeEventListener("mousemove", handleLassoMove);
    document.removeEventListener("mouseup", handleLassoEnd);

    const minX = Math.min(lassoStartX, event.clientX);
    const minY = Math.min(lassoStartY, event.clientY);
    const maxX = Math.max(lassoStartX, event.clientX);
    const maxY = Math.max(lassoStartY, event.clientY);
    const width = maxX - minX;
    const height = maxY - minY;

    if (width < 4 && height < 4) {
      if (!lassoAdditive) {
        selectedCardIds.clear();
      }
      isLassoing = false;
      lassoRender = { left: 0, top: 0, width: 0, height: 0 };
      return;
    }

    const nextSelected = new Set<string>(
      lassoAdditive ? get(selectedCardIds) : [],
    );
    const cardEls =
      cardsContainer.querySelectorAll<HTMLDivElement>(".fact-card");
    cardEls.forEach((el) => {
      const rect = el.getBoundingClientRect();
      const intersects =
        rect.right >= minX &&
        rect.left <= maxX &&
        rect.bottom >= minY &&
        rect.top <= maxY;
      if (intersects) {
        const id = el.dataset.cardId;
        if (id) nextSelected.add(id);
      }
    });

    selectedCardIds.set(nextSelected);
    isLassoing = false;
    lassoRender = { left: 0, top: 0, width: 0, height: 0 };
  }
</script>

<div class="canvas-container">
  <!-- Cork board texture overlay -->
  <div class="canvas-texture"></div>

  <div class="zoom-layer" style={`transform: scale(${$zoom})`}>
    <!-- Connections layer -->
    <Connections />

    <!-- Cards container -->
    <div
      class="cards-container"
      bind:this={cardsContainer}
      onclick={handleCanvasClick}
      onmousedown={handleLassoStart}
      onkeydown={(e) => {
        if (e.key === "Enter" || e.key === " ")
          handleCanvasClick(e as unknown as MouseEvent);
      }}
      role="button"
      tabindex="0"
      aria-label={$strings.canvas.backgroundAria}
    >
      {#if isLassoing}
        <div
          class="lasso-rect"
          style={`left:${lassoRender.left}px; top:${lassoRender.top}px; width:${lassoRender.width}px; height:${lassoRender.height}px;`}
        ></div>
      {/if}
      {#each $cards as card (card.id)}
        <Card {card} />
      {/each}
    </div>
  </div>
</div>

<style>
  .canvas-container {
    flex: 1;
    height: 100vh;
    position: relative;
    overflow: hidden;

    /* Cork board texture */
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E"),
      radial-gradient(ellipse at 30% 20%, #e6c9a8 0%, #d4a574 50%, #c49660 100%);
    background-blend-mode: soft-light, normal;
  }

  /* Additional cork texture overlay */
  .canvas-texture {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: repeating-radial-gradient(
      circle at 50% 50%,
      transparent 0,
      transparent 2px,
      rgba(139, 90, 43, 0.03) 2px,
      rgba(139, 90, 43, 0.03) 4px
    );
    pointer-events: none;
    z-index: 0;
  }

  .cards-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
  }

  .lasso-rect {
    position: absolute;
    border: 1px dashed rgba(59, 130, 246, 0.8);
    background: rgba(59, 130, 246, 0.12);
    border-radius: 6px;
    pointer-events: none;
    z-index: 30;
  }

  .zoom-layer {
    position: absolute;
    inset: 0;
    transform-origin: 50% 50%;
    transition: transform 0.15s ease;
  }

  /* Legend */
  .legend {
    position: absolute;
    bottom: 20px;
    left: 20px;
    background: rgba(255, 255, 255, 0.95);
    padding: 16px 20px;
    border-radius: 8px;
    box-shadow: var(--shadow-soft);
    z-index: 50;
    font-size: 0.85em;
  }

  .legend-title {
    font-family: "Caveat", cursive;
    font-size: 1.2em;
    margin-bottom: 10px;
    color: var(--text-dark);
  }

  .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 6px;
  }

  .legend-color {
    width: 16px;
    height: 16px;
    border-radius: 3px;
    margin-right: 10px;
  }

  .legend-label {
    color: var(--text-medium);
  }

  @media (max-width: 768px) {
    .legend {
      display: none;
    }
  }
</style>
