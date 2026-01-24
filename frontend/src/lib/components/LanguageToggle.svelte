<script lang="ts">
  import { availableLocales, locale, setLocale, strings } from '../stores/i18n';
  import type { Locale } from '../stores/i18n';

  function handleSelect(code: Locale) {
    setLocale(code);
  }
</script>

<div class="language-toggle" role="group" aria-label={$strings.language.toggleAria}>
  {#each availableLocales as item}
    <button
      class="lang-btn"
      class:active={$locale === item.code}
      aria-pressed={$locale === item.code}
      onclick={() => handleSelect(item.code)}
    >
      {item.label}
    </button>
  {/each}
</div>

<style>
  .language-toggle {
    position: fixed;
    top: 18px;
    right: 76px;
    z-index: 120;

    display: inline-flex;
    gap: 4px;
    padding: 4px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.92);
    box-shadow:
      0 6px 18px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.08);
  }

  .lang-btn {
    border: none;
    border-radius: 999px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    cursor: pointer;
    background: transparent;
    color: var(--text-light);
    transition: all 0.2s ease;
  }

  .lang-btn.active {
    background: rgba(149, 117, 205, 0.18);
    color: #4a2e8a;
  }

  .lang-btn:hover:not(.active) {
    background: rgba(0, 0, 0, 0.06);
    color: var(--text-dark);
  }

  @media (max-width: 768px) {
    .language-toggle {
      top: 14px;
      right: 64px;
    }
  }
</style>
