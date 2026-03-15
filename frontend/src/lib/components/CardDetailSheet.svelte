<script lang="ts">
  import { detailCardId, closeCardDetail } from "../stores/cardDetail";
  import { cards, connections, cardsById } from "../stores/cards";
  import { websocket } from "../stores/websocket";
  import { strings } from "../stores/i18n";
  import type { Card, Connection } from "../types";

  let card = $state<Card | null>(null);
  let cardConnections = $state<
    {
      connection: Connection;
      otherCard: Card | null;
      direction: "from" | "to";
    }[]
  >([]);
  let isAddingConnection = $state(false);
  let targetCardId = $state("");
  let connectionType = $state("relates");

  $effect(() => {
    if (!$detailCardId) {
      card = null;
      cardConnections = [];
      return;
    }

    const unsubCards = cards.subscribe((list) => {
      card = list.find((c) => c.id === $detailCardId) || null;
    });

    const unsubConnections = connections.subscribe((connList) => {
      if (!$detailCardId) {
        cardConnections = [];
        return;
      }

      const cardsMap = $cardsById;
      cardConnections = connList
        .filter(
          (conn) =>
            conn.from_id === $detailCardId || conn.to_id === $detailCardId,
        )
        .map((conn) => {
          const isFrom = conn.from_id === $detailCardId;
          const otherId = isFrom ? conn.to_id : conn.from_id;
          return {
            connection: conn,
            otherCard: cardsMap.get(otherId) || null,
            direction: isFrom ? ("to" as const) : ("from" as const),
          };
        });
    });

    return () => {
      unsubCards();
      unsubConnections();
    };
  });

  function handleDelete() {
    if (card && !card.is_root) {
      websocket.sendCardDelete(card.id);
      closeCardDetail();
    }
  }

  function handleScrimClick() {
    closeCardDetail();
  }

  function handleDeleteConnection(connectionId: string) {
    websocket.sendConnectionDelete(connectionId);
  }

  function handleAddConnection() {
    if (card && targetCardId) {
      websocket.sendConnectionCreate(card.id, targetCardId, connectionType);
      isAddingConnection = false;
      targetCardId = "";
    }
  }

  function getTypeLabel(type: string): string {
    const labels = $strings.card.typeLabels as Record<string, string>;
    return labels[type] || type;
  }

  function getTypeColor(type: string): string {
    const colors: Record<string, string> = {
      question: "var(--question-purple)",
      fact: "var(--fact-blue)",
      pain: "var(--pain-red)",
      resource: "var(--resource-green)",
      hypothesis: "var(--hypothesis-amber)",
      todo: "var(--todo-teal)",
    };
    return colors[type] || "var(--text-light)";
  }

  function getConnectionLabel(type: string, direction: "from" | "to"): string {
    const labels: Record<string, { from: string; to: string }> = {
      causes: {
        from: $strings.cardDetail?.causesTo || "causes",
        to: $strings.cardDetail?.causedBy || "caused by",
      },
      relates: {
        from: $strings.cardDetail?.relatesTo || "relates to",
        to: $strings.cardDetail?.relatedFrom || "related from",
      },
      contradicts: {
        from: $strings.cardDetail?.contradicts || "contradicts",
        to: $strings.cardDetail?.contradictedBy || "contradicted by",
      },
      blocks: {
        from: $strings.cardDetail?.blocks || "blocks",
        to: $strings.cardDetail?.blockedBy || "blocked by",
      },
    };
    return labels[type]?.[direction] || type;
  }

  function formatPercent(value: number): string {
    return Math.round(value * 100) + "%";
  }
</script>

{#if $detailCardId && card}
  <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
  <div class="sheet-scrim" onclick={handleScrimClick}></div>

  <div class="sheet">
    <div class="sheet-handle"></div>

    <button class="back-btn" onclick={closeCardDetail}>
      <svg
        width="20"
        height="20"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
      {$strings.cardDetail?.back || "Back"}
    </button>

    <div class="card-preview" style="--type-color: {getTypeColor(card.type)}">
      <div class="card-type-bar"></div>
      <div class="card-type-label">{getTypeLabel(card.type)}</div>
      <div class="card-text">{card.text}</div>
    </div>

    <div class="card-stats">
      <div class="stat-row">
        <span class="stat-label"
          >{$strings.cardDetail?.importance || "Importance"}</span
        >
        <div class="stat-bar">
          <div class="stat-fill" style="width: {card.importance * 100}%"></div>
        </div>
        <span class="stat-value">{formatPercent(card.importance)}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label"
          >{$strings.cardDetail?.confidence || "Confidence"}</span
        >
        <div class="stat-bar">
          <div
            class="stat-fill confidence"
            style="width: {card.confidence * 100}%"
          ></div>
        </div>
        <span class="stat-value">{formatPercent(card.confidence)}</span>
      </div>
    </div>

    {#if cardConnections.length > 0}
      <div class="connections-section">
        <div class="section-label">
          {$strings.cardDetail?.connections || "Connections"}
        </div>
        <div class="connections-list">
          {#each cardConnections as { connection, otherCard, direction }}
            <div class="connection-item">
              <div class="connection-row">
                <span class="connection-type"
                  >{getConnectionLabel(connection.type, direction)}</span
                >
                <button
                  class="delete-conn-btn"
                  onclick={() => handleDeleteConnection(connection.id)}
                  title="Delete connection"
                >
                  <svg
                    width="14"
                    height="14"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.5"
                  >
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              {#if otherCard}
                <button
                  class="connection-card"
                  onclick={() => {
                    if (otherCard) {
                      closeCardDetail();
                      setTimeout(() => detailCardId.set(otherCard.id), 100);
                    }
                  }}
                >
                  <span
                    class="card-type-dot"
                    style="background-color: {getTypeColor(otherCard.type)}"
                  ></span>
                  <span class="connection-text">{otherCard.text}</span>
                </button>
              {:else}
                <span class="connection-text deleted"
                  >{$strings.cardDetail?.deletedCard || "Deleted card"}</span
                >
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <div class="add-connection-section">
      {#if !isAddingConnection}
        <button
          class="add-conn-toggle"
          onclick={() => (isAddingConnection = true)}
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Add connection
        </button>
      {:else}
        <div class="add-conn-form">
          <div class="form-row">
            <select bind:value={connectionType} class="conn-type-select">
              <option value="relates">Relates to</option>
              <option value="causes">Causes</option>
              <option value="contradicts">Contradicts</option>
              <option value="blocks">Blocks</option>
            </select>
            <select bind:value={targetCardId} class="target-card-select">
              <option value="">Select card...</option>
              {#each $cards.filter((c) => c.id !== card?.id) as otherCard}
                <option value={otherCard.id}
                  >{otherCard.text.slice(0, 40)}{otherCard.text.length > 40
                    ? "..."
                    : ""}</option
                >
              {/each}
            </select>
          </div>
          <div class="form-actions">
            <button
              class="cancel-btn"
              onclick={() => (isAddingConnection = false)}>Cancel</button
            >
            <button
              class="confirm-btn"
              onclick={handleAddConnection}
              disabled={!targetCardId}>Add</button
            >
          </div>
        </div>
      {/if}
    </div>

    {#if !card.is_root}
      <button class="delete-btn" onclick={handleDelete}>
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="3 6 5 6 21 6"></polyline>
          <path
            d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
          ></path>
        </svg>
        {$strings.cardDetail?.delete || "Delete Card"}
      </button>
    {/if}
  </div>
{/if}

<style>
  .sheet-scrim {
    position: fixed;
    inset: 0;
    background: var(--bg-scrim);
    z-index: 300;
    animation: fadeIn 0.2s ease;
  }

  .sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 85vh;
    background: var(--bg-surface);
    border-radius: 20px 20px 0 0;
    z-index: 310;
    padding: 12px 20px 32px;
    overflow-y: auto;
    animation: slideUp 0.3s ease;
    box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.15);
  }

  .sheet-handle {
    width: 36px;
    height: 4px;
    background: var(--border-medium);
    border-radius: 2px;
    margin: 0 auto 16px;
  }

  .back-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 8px 12px 8px 4px;
    border: none;
    background: transparent;
    color: var(--question-purple);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 16px;
  }

  .card-preview {
    background: var(--bg-card-solid);
    border-radius: 12px;
    padding: 16px;
    box-shadow: var(--shadow-soft);
    border: 1px solid var(--border-light);
    position: relative;
    overflow: hidden;
  }

  .card-type-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--type-color);
  }

  .card-type-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--type-color);
    font-weight: 700;
    margin-bottom: 8px;
  }

  .card-text {
    font-size: 15px;
    line-height: 1.5;
    color: var(--text-dark);
  }

  .card-stats {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .stat-row {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .stat-label {
    font-size: 12px;
    color: var(--text-light);
    width: 90px;
    flex-shrink: 0;
  }

  .stat-bar {
    flex: 1;
    height: 6px;
    background: var(--border-medium);
    border-radius: 3px;
    overflow: hidden;
  }

  .stat-fill {
    height: 100%;
    background: var(--question-purple);
    border-radius: 3px;
    transition: width 0.3s ease;
  }

  .stat-fill.confidence {
    background: var(--resource-green);
  }

  .stat-value {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-medium);
    width: 40px;
    text-align: right;
  }

  .connections-section {
    margin-top: 24px;
  }

  .section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-light);
    font-weight: 600;
    margin-bottom: 10px;
  }

  .connections-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .connection-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .connection-type {
    font-size: 11px;
    color: var(--text-light);
    font-style: italic;
  }

  .connection-card {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
    background: var(--bg-surface-hover);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    text-align: left;
    transition: background 0.2s ease;
  }

  .connection-card:hover {
    background: var(--bg-surface-active);
  }

  .card-type-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .connection-text {
    font-size: 13px;
    color: var(--text-dark);
    flex: 1;
  }

  .connection-text.deleted {
    color: var(--text-light);
    font-style: italic;
  }

  .connection-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .delete-conn-btn {
    border: none;
    background: transparent;
    color: var(--text-light);
    cursor: pointer;
    padding: 2px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .delete-conn-btn:hover {
    color: var(--danger);
    background: var(--danger-subtle);
  }

  .add-connection-section {
    margin-top: 20px;
  }

  .add-conn-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border: 1px dashed var(--border-medium);
    background: transparent;
    color: var(--text-medium);
    border-radius: 8px;
    font-size: 13px;
    cursor: pointer;
    width: 100%;
    justify-content: center;
  }

  .add-conn-toggle:hover {
    background: var(--bg-surface-hover);
    border-color: var(--text-light);
  }

  .add-conn-form {
    background: var(--bg-surface-hover);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--border-light);
  }

  .form-row {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
  }

  .conn-type-select,
  .target-card-select {
    padding: 8px;
    border-radius: 6px;
    border: 1px solid var(--border-input);
    font-size: 13px;
    background: var(--bg-surface);
    color: var(--text-dark);
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
  }

  .cancel-btn {
    padding: 6px 12px;
    border: none;
    background: transparent;
    color: var(--text-light);
    font-size: 13px;
    cursor: pointer;
  }

  .confirm-btn {
    padding: 6px 16px;
    border: none;
    background: var(--question-purple);
    color: white;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
  }

  .confirm-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .delete-btn {
    margin-top: 24px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 16px;
    border: none;
    border-radius: 10px;
    background: var(--danger-subtle);
    color: var(--danger);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .delete-btn:hover {
    background: rgba(239, 68, 68, 0.18);
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slideUp {
    from {
      transform: translateY(100%);
    }
    to {
      transform: translateY(0);
    }
  }
</style>
