<script lang="ts">
  import { detailCardId, closeCardDetail } from '../stores/cardDetail';
  import { cards, connections, cardsById } from '../stores/cards';
  import { websocket } from '../stores/websocket';
  import { strings } from '../stores/i18n';
  import type { Card, Connection } from '../types';

  let card = $state<Card | null>(null);
  let cardConnections = $state<{ connection: Connection; otherCard: Card | null; direction: 'from' | 'to' }[]>([]);

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
        .filter((conn) => conn.from_id === $detailCardId || conn.to_id === $detailCardId)
        .map((conn) => {
          const isFrom = conn.from_id === $detailCardId;
          const otherId = isFrom ? conn.to_id : conn.from_id;
          return {
            connection: conn,
            otherCard: cardsMap.get(otherId) || null,
            direction: isFrom ? 'to' as const : 'from' as const
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

  function getTypeLabel(type: string): string {
    const labels = $strings.card.typeLabels as Record<string, string>;
    return labels[type] || type;
  }

  function getTypeColor(type: string): string {
    const colors: Record<string, string> = {
      question: 'var(--question-purple)',
      fact: 'var(--fact-blue)',
      pain: 'var(--pain-red)',
      resource: 'var(--resource-green)',
      hypothesis: 'var(--hypothesis-amber)'
    };
    return colors[type] || 'var(--text-light)';
  }

  function getConnectionLabel(type: string, direction: 'from' | 'to'): string {
    const labels: Record<string, { from: string; to: string }> = {
      causes: { from: $strings.cardDetail?.causesTo || 'causes', to: $strings.cardDetail?.causedBy || 'caused by' },
      relates: { from: $strings.cardDetail?.relatesTo || 'relates to', to: $strings.cardDetail?.relatedFrom || 'related from' },
      contradicts: { from: $strings.cardDetail?.contradicts || 'contradicts', to: $strings.cardDetail?.contradictedBy || 'contradicted by' },
      blocks: { from: $strings.cardDetail?.blocks || 'blocks', to: $strings.cardDetail?.blockedBy || 'blocked by' }
    };
    return labels[type]?.[direction] || type;
  }

  function formatPercent(value: number): string {
    return Math.round(value * 100) + '%';
  }
</script>

{#if $detailCardId && card}
  <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
  <div class="sheet-scrim" onclick={handleScrimClick}></div>

  <div class="sheet">
    <div class="sheet-handle"></div>

    <button class="back-btn" onclick={closeCardDetail}>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
      {$strings.cardDetail?.back || 'Back'}
    </button>

    <div class="card-preview" style="--type-color: {getTypeColor(card.type)}">
      <div class="card-type-bar"></div>
      <div class="card-type-label">{getTypeLabel(card.type)}</div>
      <div class="card-text">{card.text}</div>
    </div>

    <div class="card-stats">
      <div class="stat-row">
        <span class="stat-label">{$strings.cardDetail?.importance || 'Importance'}</span>
        <div class="stat-bar">
          <div class="stat-fill" style="width: {card.importance * 100}%"></div>
        </div>
        <span class="stat-value">{formatPercent(card.importance)}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">{$strings.cardDetail?.confidence || 'Confidence'}</span>
        <div class="stat-bar">
          <div class="stat-fill confidence" style="width: {card.confidence * 100}%"></div>
        </div>
        <span class="stat-value">{formatPercent(card.confidence)}</span>
      </div>
    </div>

    {#if cardConnections.length > 0}
      <div class="connections-section">
        <div class="section-label">{$strings.cardDetail?.connections || 'Connections'}</div>
        <div class="connections-list">
          {#each cardConnections as { connection, otherCard, direction }}
            <div class="connection-item">
              <span class="connection-type">{getConnectionLabel(connection.type, direction)}</span>
              {#if otherCard}
                <button class="connection-card" onclick={() => { if (otherCard) { closeCardDetail(); setTimeout(() => detailCardId.set(otherCard.id), 100); } }}>
                  <span class="card-type-dot" style="background-color: {getTypeColor(otherCard.type)}"></span>
                  <span class="connection-text">{otherCard.text}</span>
                </button>
              {:else}
                <span class="connection-text deleted">{$strings.cardDetail?.deletedCard || 'Deleted card'}</span>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    {#if !card.is_root}
      <button class="delete-btn" onclick={handleDelete}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="3 6 5 6 21 6"></polyline>
          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
        </svg>
        {$strings.cardDetail?.delete || 'Delete Card'}
      </button>
    {/if}
  </div>
{/if}

<style>
  .sheet-scrim {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 300;
    animation: fadeIn 0.2s ease;
  }

  .sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    max-height: 85vh;
    background: #fff;
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
    background: rgba(0, 0, 0, 0.15);
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
    background: #fefefe;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.06);
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
    background: rgba(0, 0, 0, 0.08);
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
    background: rgba(0, 0, 0, 0.03);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    text-align: left;
    transition: background 0.2s ease;
  }

  .connection-card:hover {
    background: rgba(0, 0, 0, 0.06);
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
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s ease;
  }

  .delete-btn:hover {
    background: rgba(239, 68, 68, 0.18);
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
  }
</style>
