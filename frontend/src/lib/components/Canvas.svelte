<script lang="ts">
  import { cards } from '../stores/cards';
  import { selectedCardId } from '../stores/selection';
  import Card from './Card.svelte';

  function handleCanvasClick(e: MouseEvent) {
    // Deselect if clicked on cards-container (not on a card)
    const target = e.target as HTMLElement;
    if (target.classList.contains('cards-container')) {
      selectedCardId.deselect();
    }
  }
</script>

<div class="canvas-container">
  <!-- Cork board texture overlay -->
  <div class="canvas-texture"></div>

  <!-- Legend -->
  <div class="legend">
    <div class="legend-title">Card Types</div>
    <div class="legend-item">
      <div class="legend-color" style="background: var(--question-purple);"></div>
      <span class="legend-label">Question</span>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: var(--fact-blue);"></div>
      <span class="legend-label">Fact</span>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: var(--pain-red);"></div>
      <span class="legend-label">Pain</span>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: var(--resource-green);"></div>
      <span class="legend-label">Resource</span>
    </div>
    <div class="legend-item">
      <div class="legend-color" style="background: var(--hypothesis-amber);"></div>
      <span class="legend-label">Hypothesis</span>
    </div>
  </div>

  <!-- Cards container -->
  <div class="cards-container" onclick={handleCanvasClick}>
    {#each $cards as card (card.id)}
      <Card {card} />
    {/each}
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
    font-family: 'Caveat', cursive;
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
</style>
