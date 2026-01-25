<script lang="ts" module>
  // Shared counter across all Card instances
  let globalZIndex = 10;
</script>

<script lang="ts">
  import type { Card } from "../types";
  import { websocket } from "../stores/websocket";
  import { cards, connections } from "../stores/cards";
  import { selectedCardIds } from "../stores/selection";
  import { strings } from "../stores/i18n";
  import { isMobile } from "../stores/mobile";
  import { openCardDetail } from "../stores/cardDetail";
  import { session } from "../stores/session";
  import { get } from "svelte/store";

  interface Props {
    card: Card;
  }

  let { card }: Props = $props();

  let cardEl: HTMLDivElement;
  let isDragging = $state(false);
  let hasMoved = false;
  let isEditing = $state(false);
  let editText = $state("");
  let editEl: HTMLTextAreaElement | null = null;

  // Selection from global store
  const isSelected = $derived($selectedCardIds.has(card.id));
  let zIndex = $state(10);
  let dragStartX = 0;
  let dragStartY = 0;
  let initialX = 0;
  let initialY = 0;
  let dragGroupIds: string[] = [];
  let dragGroupStart = new Map<string, { x: number; y: number }>();
  let isResizing = $state(false);
  let resizeGroupScaleStart = new Map<string, number>();

  // Can delete if selected and not root card
  const canDelete = $derived(
    isSelected && !card.is_root && $selectedCardIds.size <= 1,
  );

  // Focus Mode: Dim if something is selected BUT not this card AND not connected to it
  const isDimmed = $derived(
    $selectedCardIds.size > 0 &&
      !isSelected &&
      !$connections.some((c) => {
        const isConnectedToSelection =
          ($selectedCardIds.has(c.from_id) && c.to_id === card.id) ||
          ($selectedCardIds.has(c.to_id) && c.from_id === card.id);
        return isConnectedToSelection;
      }),
  );

  // Calculate scale based on importance (0.7 to 1.3) AND custom scale
  const scale = $derived(
    (0.7 + card.importance * 0.6) * (card.custom_scale || 1),
  );

  // Stable rotation based on card.id for handmade feel
  function getRotation(id: string): number {
    let hash = 0;
    for (let i = 0; i < id.length; i++) {
      hash = (hash << 5) - hash + id.charCodeAt(i);
      hash |= 0;
    }
    return ((hash % 100) / 100 - 0.5) * 6;
  }
  let rotation = $derived(card.is_root ? 0 : getRotation(card.id));

  // Highlight color based on card type
  const highlightColors: Record<string, string> = {
    fact: "rgba(91, 155, 213, 0.5)",
    pain: "rgba(229, 115, 115, 0.5)",
    resource: "rgba(129, 199, 132, 0.5)",
    hypothesis: "rgba(255, 183, 77, 0.5)",
    question: "rgba(149, 117, 205, 0.5)",
    todo: "rgba(20, 184, 166, 0.5)",
  };

  function handleMouseDown(e: MouseEvent) {
    if (e.button !== 0) return;
    if (isEditing) return;
    const isMultiToggle = e.shiftKey || e.metaKey || e.ctrlKey;
    if (!get(selectedCardIds).has(card.id)) {
      if (isMultiToggle) {
        selectedCardIds.add(card.id);
      } else {
        selectedCardIds.selectOnly(card.id);
      }
    }
    startDrag(e.clientX, e.clientY);
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    e.preventDefault();
  }

  function handleTouchStart(e: TouchEvent) {
    const touch = e.touches[0];
    if (isEditing) return;
    if (!get(selectedCardIds).has(card.id)) {
      selectedCardIds.selectOnly(card.id);
    }
    startDrag(touch.clientX, touch.clientY);
    document.addEventListener("touchmove", handleTouchMove, { passive: false });
    document.addEventListener("touchend", handleTouchEnd);
    e.preventDefault();
  }

  function startDrag(clientX: number, clientY: number) {
    isDragging = true;
    hasMoved = false;
    dragStartX = clientX;
    dragStartY = clientY;
    dragGroupIds = Array.from(get(selectedCardIds));
    dragGroupStart = new Map();

    // Bring card to front
    globalZIndex++;
    zIndex = globalZIndex;

    const canvasEl = cardEl.parentElement;
    if (!canvasEl) return;

    const canvasRect = canvasEl.getBoundingClientRect();
    initialX = (card.x / 100) * canvasRect.width;
    initialY = (card.y / 100) * canvasRect.height;
    const cardList = get(cards);
    for (const id of dragGroupIds) {
      const cardItem = cardList.find((item) => item.id === id);
      if (!cardItem) continue;
      dragGroupStart.set(id, {
        x: (cardItem.x / 100) * canvasRect.width,
        y: (cardItem.y / 100) * canvasRect.height,
      });
    }
  }

  function handleMouseMove(e: MouseEvent) {
    if (!isDragging) return;
    updatePosition(e.clientX, e.clientY);
  }

  function handleTouchMove(e: TouchEvent) {
    if (!isDragging) return;
    const touch = e.touches[0];
    updatePosition(touch.clientX, touch.clientY);
    e.preventDefault();
  }

  function updatePosition(clientX: number, clientY: number) {
    const canvasEl = cardEl.parentElement;
    if (!canvasEl) return;

    const canvasRect = canvasEl.getBoundingClientRect();
    const dx = clientX - dragStartX;
    const dy = clientY - dragStartY;

    // Mark as moved if moved more than 5px
    if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
      hasMoved = true;
    }

    if (dragGroupIds.length > 1) {
      const updates = dragGroupIds.map((id) => {
        const start = dragGroupStart.get(id);
        if (!start) return null;
        const newX = ((start.x + dx) / canvasRect.width) * 100;
        const newY = ((start.y + dy) / canvasRect.height) * 100;
        return {
          id,
          x: Math.max(5, Math.min(95, newX)),
          y: Math.max(5, Math.min(95, newY)),
        };
      });
      updates.forEach((update) => {
        if (!update) return;
        cards.updateCard(update.id, { x: update.x, y: update.y });
      });
    } else {
      const newX = ((initialX + dx) / canvasRect.width) * 100;
      const newY = ((initialY + dy) / canvasRect.height) * 100;

      // Clamp to bounds
      const clampedX = Math.max(5, Math.min(95, newX));
      const clampedY = Math.max(5, Math.min(95, newY));

      // Update local store immediately for smooth dragging
      cards.updateCard(card.id, { x: clampedX, y: clampedY });
    }
  }

  function handleMouseUp(e: MouseEvent) {
    endDrag(e);
    document.removeEventListener("mousemove", handleMouseMove);
    document.removeEventListener("mouseup", handleMouseUp);
  }

  function handleTouchEnd() {
    endDrag();
    document.removeEventListener("touchmove", handleTouchMove);
    document.removeEventListener("touchend", handleTouchEnd);
  }

  function endDrag(event?: MouseEvent) {
    if (!isDragging) return;
    isDragging = false;

    // If no movement, toggle selection (or open detail on mobile)
    if (!hasMoved) {
      if (get(isMobile)) {
        openCardDetail(card.id);
      } else {
        const isMultiToggle =
          event?.shiftKey || event?.metaKey || event?.ctrlKey;
        if (isMultiToggle) {
          selectedCardIds.toggle(card.id);
        } else {
          selectedCardIds.selectOnly(card.id);
        }
      }
      return;
    }

    // Mark as pinned and send to server
    const cardList = get(cards);
    if (dragGroupIds.length > 1) {
      for (const id of dragGroupIds) {
        const cardItem = cardList.find((item) => item.id === id);
        if (!cardItem) continue;
        cards.updateCard(id, { pinned: true });
        websocket.sendCardMove(id, cardItem.x, cardItem.y, true);
      }
    } else {
      cards.updateCard(card.id, { pinned: true });
      websocket.sendCardMove(card.id, card.x, card.y, true);
    }
  }

  function handleDelete(e: MouseEvent) {
    e.stopPropagation();
    selectedCardIds.clear();
    websocket.sendCardDelete(card.id);
  }

  function startEditing(e: MouseEvent) {
    e.stopPropagation();
    if (get(isMobile)) return;
    if (card.is_root && get(session).phase !== "question") return;
    isEditing = true;
    editText = card.text;
    selectedCardIds.selectOnly(card.id);
    requestAnimationFrame(() => editEl?.focus());
  }

  function cancelEdit() {
    isEditing = false;
    editText = card.text;
  }

  function commitEdit() {
    const next = editText.trim();
    if (!next) {
      cancelEdit();
      return;
    }
    isEditing = false;
    if (next !== card.text) {
      cards.updateCard(card.id, { text: next });
      websocket.sendCardUpdate(card.id, { text: next });
    }
  }

  function handleEditKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      commitEdit();
    } else if (event.key === "Escape") {
      event.preventDefault();
      cancelEdit();
    }
  }

  function handleResizeMouseDown(e: MouseEvent) {
    if (e.button !== 0) return;
    e.stopPropagation();
    e.preventDefault();

    isResizing = true;
    dragStartX = e.clientX;
    dragStartY = e.clientY;

    const selectedIds = Array.from(get(selectedCardIds));
    const cardList = get(cards);

    if (!selectedIds.includes(card.id)) {
      selectedCardIds.selectOnly(card.id);
    }

    const currentSelectedIds = Array.from(get(selectedCardIds));
    resizeGroupScaleStart = new Map();

    for (const id of currentSelectedIds) {
      const cardItem = cardList.find((item) => item.id === id);
      if (!cardItem) continue;
      resizeGroupScaleStart.set(id, cardItem.custom_scale || 1.0);
    }

    document.addEventListener("mousemove", handleResizeMove);
    document.addEventListener("mouseup", handleResizeUp);
  }

  function handleResizeMove(e: MouseEvent) {
    if (!isResizing) return;

    const dx = e.clientX - dragStartX;
    const dy = e.clientY - dragStartY;

    // We use the diagonal movement to determine scale change
    const scaleDelta = (dx + dy) / 200;

    const selectedIds = Array.from(resizeGroupScaleStart.keys());

    for (const id of selectedIds) {
      const startScale = resizeGroupScaleStart.get(id);
      if (startScale === undefined) continue;

      const newScale = Math.max(0.5, startScale + scaleDelta);
      cards.updateCard(id, { custom_scale: newScale });
    }
  }

  function handleResizeUp() {
    if (!isResizing) return;
    isResizing = false;

    const selectedIds = Array.from(resizeGroupScaleStart.keys());
    const cardList = get(cards);

    for (const id of selectedIds) {
      const cardItem = cardList.find((item) => item.id === id);
      if (!cardItem) continue;

      websocket.sendCardMove(
        id,
        cardItem.x,
        cardItem.y,
        true,
        undefined,
        undefined,
        cardItem.custom_scale,
      );
    }

    document.removeEventListener("mousemove", handleResizeMove);
    document.removeEventListener("mouseup", handleResizeUp);
  }
</script>

<div
  bind:this={cardEl}
  class="fact-card"
  class:is-new={card.is_new}
  class:is-root={card.is_root}
  class:is-dragging={isDragging}
  class:is-selected={isSelected}
  class:is-dimmed={isDimmed}
  class:is-deleting={card.is_deleting}
  data-type={card.type}
  data-card-id={card.id}
  style="
    left: {card.x}%;
    top: {card.y}%;
    z-index: {zIndex};
    --rotation: {rotation}deg;
    --scale: {scale};
    --highlight-color: {highlightColors[card.type]};
  "
  onmousedown={handleMouseDown}
  ontouchstart={handleTouchStart}
  role="button"
  tabindex="0"
>
  {#if canDelete}
    <button
      class="delete-btn"
      onclick={handleDelete}
      onmousedown={(e) => e.stopPropagation()}
      ontouchstart={(e) => e.stopPropagation()}
      aria-label="Delete card">×</button
    >
  {/if}
  <span class="card-emoji">{card.emoji}</span>
  {#if isEditing}
    <textarea
      class="card-edit"
      bind:this={editEl}
      bind:value={editText}
      rows="3"
      onkeydown={handleEditKeydown}
      onblur={commitEdit}
    ></textarea>
  {:else}
    <p class="card-text" ondblclick={startEditing}>{card.text}</p>
  {/if}
  <span class="card-type-label">{$strings.card.typeLabels[card.type]}</span>
  <div
    class="resize-handle"
    onmousedown={handleResizeMouseDown}
    role="button"
    tabindex="-1"
    aria-label="Resize"
  ></div>
</div>

<style>
  .fact-card {
    position: absolute;
    padding: 16px 20px;
    border-radius: 4px;
    cursor: move;
    z-index: 10;
    max-width: 220px;
    min-width: 160px;
    transform: translate(-50%, -50%) scale(var(--scale, 1))
      rotate(var(--rotation, 0deg));
    user-select: none;

    /* Paper texture effect */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.95) 0%,
      rgba(255, 255, 255, 0.85) 100%
    );

    box-shadow:
      var(--shadow-card),
      inset 0 0 30px rgba(0, 0, 0, 0.02);

    /* Paper grain */
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='grain'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23grain)' opacity='0.03'/%3E%3C/svg%3E"),
      linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.95) 0%,
        rgba(255, 255, 255, 0.85) 100%
      );

    transition:
      box-shadow 0.2s ease,
      opacity 0.3s ease,
      filter 0.3s ease;
    animation: cardAppear 0.4s ease-out forwards;
  }

  .fact-card.is-dimmed {
    opacity: 0.15;
    filter: grayscale(0.8) blur(0.5px);
    pointer-events: none; /* Let clicks pass through to canvas to deselect */
    z-index: 1 !important; /* Push to back */
  }

  .fact-card:hover {
    box-shadow:
      0 6px 20px rgba(0, 0, 0, 0.2),
      0 2px 6px rgba(0, 0, 0, 0.15);
    z-index: 100;
  }

  .fact-card.is-dragging {
    cursor: grabbing;
    z-index: 1000;
    box-shadow:
      0 10px 30px rgba(0, 0, 0, 0.25),
      0 4px 10px rgba(0, 0, 0, 0.2);
  }

  /* Pin effect on cards */
  .fact-card::before {
    content: "";
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
    box-shadow: var(--shadow-pin);
    z-index: 11;
  }

  /* Card type indicator - tape strip */
  .fact-card::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    border-radius: 4px 4px 0 0;
  }

  /* Card type styles */
  .fact-card[data-type="fact"]::after {
    background: var(--fact-blue);
  }
  .fact-card[data-type="pain"]::after {
    background: var(--pain-red);
  }
  .fact-card[data-type="resource"]::after {
    background: var(--resource-green);
  }
  .fact-card[data-type="hypothesis"]::after {
    background: var(--hypothesis-amber);
  }
  .fact-card[data-type="question"]::after {
    background: var(--question-purple);
  }
  .fact-card[data-type="todo"]::after {
    background: var(--todo-teal);
  }

  .fact-card[data-type="fact"] {
    background-color: var(--fact-blue-light);
  }
  .fact-card[data-type="pain"] {
    background-color: var(--pain-red-light);
  }
  .fact-card[data-type="resource"] {
    background-color: var(--resource-green-light);
  }
  .fact-card[data-type="hypothesis"] {
    background-color: var(--hypothesis-amber-light);
  }
  .fact-card[data-type="question"] {
    background-color: var(--question-purple-light);
  }
  .fact-card[data-type="todo"] {
    background-color: var(--todo-teal-light);
  }

  /* Question card - special styling (center) */
  .fact-card.is-root {
    min-width: 240px;
    padding: 24px;
    font-size: 1.1em;
    text-align: center;
  }

  .fact-card.is-root::before {
    width: 20px;
    height: 20px;
    background: radial-gradient(circle at 30% 30%, #b39ddb, #7e57c2);
  }

  .card-emoji {
    font-size: 1.8em;
    margin-bottom: 8px;
    display: block;
    filter: drop-shadow(1px 1px 1px rgba(0, 0, 0, 0.1));
  }

  .card-text {
    color: var(--text-dark);
    font-size: 0.95em;
    line-height: 1.4;
    font-family: Georgia, serif;
  }

  .card-edit {
    width: 100%;
    min-height: 64px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    padding: 6px 8px;
    font-size: 0.95em;
    line-height: 1.4;
    font-family: Georgia, serif;
    color: var(--text-dark);
    background: rgba(255, 255, 255, 0.8);
    resize: none;
  }

  .card-edit:focus {
    outline: 2px solid rgba(59, 130, 246, 0.5);
  }

  .card-type-label {
    position: absolute;
    bottom: 8px;
    right: 12px;
    font-size: 0.7em;
    color: var(--text-light);
    font-family: "Caveat", cursive;
    text-transform: lowercase;
  }

  /* New card highlight animation */
  .fact-card.is-new {
    animation:
      cardAppear 0.4s ease-out forwards,
      newCardPulse 0.8s ease-in-out 0.4s 3;
    z-index: 50;
  }

  /* Selected card */
  .fact-card.is-selected {
    outline: 3px solid rgba(59, 130, 246, 0.7);
    outline-offset: 2px;
  }

  /* Delete button */
  .delete-btn {
    position: absolute;
    top: -8px;
    right: -8px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #ef4444;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 18px;
    line-height: 22px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    z-index: 12;
    transition:
      transform 0.1s,
      background 0.1s;
  }

  .delete-btn:hover {
    transform: scale(1.1);
    background: #dc2626;
  }

  .delete-btn:active {
    transform: scale(0.95);
  }

  /* Deleting card - fade-out animation */
  .fact-card.is-deleting {
    animation: cardFadeOut 0.5s ease-out forwards;
    pointer-events: none;
  }

  @keyframes cardFadeOut {
    0% {
      opacity: 1;
      transform: translate(-50%, -50%) scale(var(--scale, 1))
        rotate(var(--rotation, 0deg));
    }
    100% {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.7) rotate(var(--rotation, 0deg));
    }
  }

  .resize-handle {
    position: absolute;
    bottom: 0;
    right: 0;
    width: 20px;
    height: 20px;
    cursor: nwse-resize;
    z-index: 20;
    border-radius: 0 0 4px 0;
    background: linear-gradient(
      135deg,
      transparent 50%,
      rgba(0, 0, 0, 0.05) 50%,
      rgba(0, 0, 0, 0.05) 60%,
      transparent 60%,
      transparent 70%,
      rgba(0, 0, 0, 0.05) 70%
    );
  }

  .resize-handle:hover {
    background: linear-gradient(
      135deg,
      transparent 50%,
      rgba(59, 130, 246, 0.2) 50%
    );
  }
</style>
