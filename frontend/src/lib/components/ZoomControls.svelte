<script lang="ts">
  import { zoom, ZOOM_MAX, ZOOM_MIN } from '../stores/zoom';
  import { strings } from '../stores/i18n';

  function zoomIn() {
    zoom.zoomIn();
  }

  function zoomOut() {
    zoom.zoomOut();
  }
</script>

<div class="zoom-controls" aria-label={$strings.zoom.controlsAria}>
  <button
    class="zoom-btn"
    onclick={zoomIn}
    disabled={$zoom >= ZOOM_MAX}
    title={$strings.zoom.inTitle}
    aria-label={$strings.zoom.inAria}
  >
    +
  </button>
  <button
    class="zoom-btn"
    onclick={zoomOut}
    disabled={$zoom <= ZOOM_MIN}
    title={$strings.zoom.outTitle}
    aria-label={$strings.zoom.outAria}
  >
    −
  </button>
</div>

<style>
  .zoom-controls {
    position: fixed;
    top: 72px;
    right: 20px;
    z-index: 120;

    display: grid;
    gap: 8px;
  }

  .zoom-btn {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    background: #ffffff;
    color: var(--text-dark);
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    box-shadow:
      0 6px 18px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .zoom-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow:
      0 8px 22px rgba(0, 0, 0, 0.14),
      0 4px 10px rgba(0, 0, 0, 0.1);
  }

  .zoom-btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  @media (max-width: 768px) {
    .zoom-controls {
      top: 64px;
      right: 12px;
    }
  }
</style>
