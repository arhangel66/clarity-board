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
    top: 70px;
    right: 20px;
    z-index: 120;

    display: grid;
    gap: 8px;
  }

  .lang-btn {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    background: #ffffff;
    color: var(--text-dark);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.3px;
    cursor: pointer;
    box-shadow:
      0 6px 18px rgba(0, 0, 0, 0.12),
      0 2px 8px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  }

  .lang-btn:hover:not(.active) {
    transform: translateY(-1px);
    box-shadow:
      0 8px 22px rgba(0, 0, 0, 0.14),
      0 4px 10px rgba(0, 0, 0, 0.1);
  }

  .lang-btn.active {
    background: rgba(149, 117, 205, 0.18);
    color: #4a2e8a;
    border-color: rgba(149, 117, 205, 0.3);
  }

  @media (max-width: 768px) {
    .language-toggle {
      display: none;
    }
  }
</style>
