<script lang="ts">
  import { Check, X } from "lucide-svelte";
  import { derived } from "svelte/store";

  import { trackUpgradeClicked } from "../analytics";
  import { access, getAccessPaywallGate } from "../stores/access";
  import { strings } from "../stores/i18n";

  type Props = {
    viewerId?: string | null;
  };

  const PAYWALL_ENTRY_STORAGE_KEY = "fact.paywall.entry.v1";

  let { viewerId = null }: Props = $props();
  let isOpen = $state(false);
  let lastHandledPromptCount: number | null = $state(null);
  let selectedPlan: string | null = $state(null);

  const paywallState = derived([access, strings], ([$access, $strings]) => {
    const pricing = $strings.landing.pricing;
    const labels = $strings.access;
    const gate = getAccessPaywallGate($access.snapshot);

    return {
      ...gate,
      pricing,
      labels,
    };
  });

  function readSeenEntryKey(): string | null {
    if (typeof window === "undefined") {
      return null;
    }

    try {
      return window.sessionStorage.getItem(PAYWALL_ENTRY_STORAGE_KEY);
    } catch {
      return null;
    }
  }

  function persistSeenEntryKey(entryKey: string) {
    if (typeof window === "undefined") {
      return;
    }

    try {
      window.sessionStorage.setItem(PAYWALL_ENTRY_STORAGE_KEY, entryKey);
    } catch {
      // Ignore storage failures; current-mount behavior still works.
    }
  }

  function buildEntryStorageKey(gateKey: string, currentViewerId: string | null) {
    return `${currentViewerId ?? "anonymous"}:${gateKey}`;
  }

  $effect(() => {
    const promptCount = $access.paywallPromptCount;

    if (lastHandledPromptCount === null) {
      lastHandledPromptCount = promptCount;
    }

    if (!$paywallState.shouldShow) {
      isOpen = false;
      selectedPlan = null;
      lastHandledPromptCount = promptCount;
      return;
    }

    const entryStorageKey = buildEntryStorageKey($paywallState.key, viewerId);
    const hasSeenEntry = readSeenEntryKey() === entryStorageKey;
    const hasNewBlockedPrompt = promptCount > (lastHandledPromptCount ?? promptCount);

    if (!hasSeenEntry) {
      persistSeenEntryKey(entryStorageKey);
      isOpen = true;
      selectedPlan = null;
    } else if (hasNewBlockedPrompt) {
      isOpen = true;
      selectedPlan = null;
    }

    lastHandledPromptCount = promptCount;
  });

  function closeModal() {
    isOpen = false;
    selectedPlan = null;
  }

  function previewPlan(planId: string, planName: string) {
    trackUpgradeClicked(planId, "paywall_modal");
    selectedPlan = planName;
  }

  function handleWindowKeydown(event: KeyboardEvent) {
    if (event.key === "Escape" && isOpen) {
      closeModal();
    }
  }
</script>

<svelte:window onkeydown={handleWindowKeydown} />

{#if isOpen}
  <button
    class="paywall-scrim"
    type="button"
    aria-label={$paywallState.labels.paywallCloseAria}
    onclick={closeModal}
  ></button>

  <div
    class="paywall-modal"
    role="dialog"
    aria-modal="true"
    aria-labelledby="paywall-title"
    aria-describedby="paywall-body"
  >
    <button
      class="paywall-close"
      type="button"
      aria-label={$paywallState.labels.paywallCloseAria}
      onclick={closeModal}
    >
      <X size={18} strokeWidth={2.4} />
    </button>

    <div class="paywall-kicker">{$paywallState.labels.kicker}</div>
    <h2 class="paywall-title" id="paywall-title">
      {$paywallState.labels.paywallTitle.replace("{total}", String($paywallState.total))}
    </h2>
    <p class="paywall-body" id="paywall-body">
      {$paywallState.labels.paywallBody}
    </p>
    <p class="paywall-note">{$paywallState.labels.paywallNote}</p>

    <div class="paywall-grid">
      {#each $paywallState.pricing.plans as plan}
        <article class="paywall-card" class:featured={plan.featured}>
          <div class="paywall-card-head">
            <span class="paywall-badge" class:featured={plan.featured}>
              {plan.badge}
            </span>
            <h3 class="paywall-plan-name">{plan.name}</h3>
            <div class="paywall-price-row">
              <span class="paywall-price">{plan.price}</span>
              <span class="paywall-period">{plan.period}</span>
            </div>
            <p class="paywall-description">{plan.description}</p>
          </div>

          <ul class="paywall-features">
            {#each plan.features as feature}
              <li class="paywall-feature">
                <span class="paywall-check">
                  <Check size={16} strokeWidth={2.4} />
                </span>
                <span>{feature}</span>
              </li>
            {/each}
          </ul>

          <button
            class="paywall-cta"
            class:featured={plan.featured}
            type="button"
            onclick={() => previewPlan(plan.id, plan.name)}
          >
            {plan.cta}
          </button>
        </article>
      {/each}
    </div>

    {#if selectedPlan}
      <p class="paywall-preview">
        {$paywallState.labels.paywallPreview.replace("{plan}", selectedPlan)}
      </p>
    {/if}

    <div class="paywall-actions">
      <button class="paywall-dismiss" type="button" onclick={closeModal}>
        {$paywallState.labels.paywallDismiss}
      </button>
    </div>
  </div>
{/if}

<style>
  .paywall-scrim {
    position: fixed;
    inset: 0;
    z-index: 260;
    padding: 0;
    border: none;
    background: rgba(32, 24, 15, 0.56);
    backdrop-filter: blur(6px);
  }

  .paywall-modal {
    position: fixed;
    inset: 50% auto auto 50%;
    transform: translate(-50%, -50%);
    z-index: 270;
    width: min(920px, calc(100vw - 32px));
    max-height: calc(100vh - 32px);
    overflow: auto;
    padding: 28px;
    border-radius: 28px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(252, 248, 242, 0.98));
    box-shadow: 0 28px 80px rgba(24, 18, 10, 0.24);
    color: var(--text-dark);
  }

  .paywall-close {
    position: absolute;
    top: 18px;
    right: 18px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border: none;
    border-radius: 999px;
    background: rgba(107, 77, 34, 0.08);
    color: var(--text-medium);
    cursor: pointer;
    transition: background 0.2s ease, color 0.2s ease;
  }

  .paywall-close:hover {
    background: rgba(107, 77, 34, 0.14);
    color: var(--text-dark);
  }

  .paywall-kicker {
    margin-bottom: 10px;
    color: #8d5a18;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .paywall-title {
    margin: 0 0 12px;
    font-size: clamp(1.85rem, 2.5vw, 2.4rem);
    line-height: 1.08;
  }

  .paywall-body {
    margin: 0;
    color: var(--text-medium);
    font-size: 1rem;
    line-height: 1.65;
  }

  .paywall-note {
    margin: 12px 0 0;
    color: #6a5335;
    font-size: 0.95rem;
    line-height: 1.55;
  }

  .paywall-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-top: 24px;
  }

  .paywall-card {
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding: 20px;
    border-radius: 22px;
    border: 1px solid rgba(82, 56, 23, 0.12);
    background: rgba(255, 255, 255, 0.9);
  }

  .paywall-card.featured {
    border-color: rgba(140, 94, 33, 0.28);
    background: linear-gradient(180deg, #fff4df, #ffffff);
    box-shadow: 0 16px 34px rgba(140, 94, 33, 0.14);
  }

  .paywall-card-head {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .paywall-badge {
    display: inline-flex;
    align-self: flex-start;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(141, 90, 24, 0.1);
    color: #8d5a18;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .paywall-badge.featured {
    background: rgba(141, 90, 24, 0.16);
  }

  .paywall-plan-name {
    margin: 0;
    font-size: 1.2rem;
  }

  .paywall-price-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .paywall-price {
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1;
  }

  .paywall-period {
    color: var(--text-medium);
    font-size: 0.92rem;
  }

  .paywall-description {
    margin: 0;
    color: var(--text-medium);
    font-size: 0.95rem;
    line-height: 1.55;
  }

  .paywall-features {
    display: grid;
    gap: 10px;
    margin: 0;
    padding: 0;
    list-style: none;
  }

  .paywall-feature {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    color: var(--text-medium);
    font-size: 0.92rem;
    line-height: 1.45;
  }

  .paywall-check {
    flex-shrink: 0;
    margin-top: 2px;
    color: var(--color-card-resource);
  }

  .paywall-cta,
  .paywall-dismiss {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 46px;
    border: none;
    border-radius: 999px;
    font-size: 0.96rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  }

  .paywall-cta {
    margin-top: auto;
    background: rgba(107, 77, 34, 0.08);
    color: var(--text-dark);
  }

  .paywall-cta.featured {
    background: linear-gradient(135deg, #8d5a18, #c07f2b);
    box-shadow: 0 14px 28px rgba(141, 90, 24, 0.18);
    color: white;
  }

  .paywall-cta:hover,
  .paywall-dismiss:hover {
    transform: translateY(-1px);
  }

  .paywall-preview {
    margin: 20px 0 0;
    padding: 14px 16px;
    border-radius: 18px;
    background: rgba(248, 225, 183, 0.34);
    color: #6a5335;
    font-size: 0.94rem;
    line-height: 1.55;
  }

  .paywall-actions {
    margin-top: 18px;
  }

  .paywall-dismiss {
    background: rgba(107, 77, 34, 0.08);
    color: var(--text-dark);
  }

  @media (max-width: 900px) {
    .paywall-modal {
      width: min(640px, calc(100vw - 24px));
      padding: 22px;
    }

    .paywall-grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 640px) {
    .paywall-modal {
      inset: auto 12px 12px 12px;
      transform: none;
      width: auto;
      max-height: calc(100vh - 24px);
      padding: 20px 18px 18px;
      border-radius: 24px;
    }

    .paywall-title {
      padding-right: 30px;
      font-size: 1.7rem;
    }
  }
</style>
