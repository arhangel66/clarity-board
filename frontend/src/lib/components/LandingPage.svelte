<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '../stores/auth';
  import { strings, locale, setLocale, availableLocales } from '../stores/i18n';
  import type { Locale } from '../stores/i18n';

  let openFaqIndex = $state(-1);

  function handleLogin() {
    auth.loginWithGoogle();
  }

  function handleLocale(code: Locale) {
    setLocale(code);
  }

  function toggleFaq(index: number) {
    openFaqIndex = openFaqIndex === index ? -1 : index;
  }

  onMount(() => {
    const root = document.documentElement;
    root.classList.add('landing-active');
    document.body.classList.add('landing-active');
    return () => {
      root.classList.remove('landing-active');
      document.body.classList.remove('landing-active');
    };
  });
</script>

<div class="landing-root">
  <!-- ============ NAV ============ -->
  <nav class="nav">
    <div class="nav-logo">{$strings.landing.kicker}</div>
    <div class="nav-right">
      <div class="lang-toggle" role="group" aria-label={$strings.language.toggleAria}>
        {#each availableLocales as item}
          <button
            class="lang-btn"
            class:active={$locale === item.code}
            aria-pressed={$locale === item.code}
            onclick={() => handleLocale(item.code)}
          >
            {item.label}
          </button>
        {/each}
      </div>
      <button class="nav-cta" onclick={handleLogin}>
        {$strings.landing.cta}
      </button>
    </div>
  </nav>

  <!-- ============ HERO ============ -->
  <section class="hero">
    <div class="hero-bg">
      <div class="hero-orb hero-orb-1"></div>
      <div class="hero-orb hero-orb-2"></div>
      <div class="hero-orb hero-orb-3"></div>
      <div class="hero-grain"></div>
    </div>

    <div class="hero-inner">
      <div class="hero-copy">
        <div class="hero-badge">
          <span class="hero-badge-dot"></span>
          {$strings.landing.kicker}
        </div>
        <h1 class="hero-title">{$strings.landing.titleA}</h1>
        <p class="hero-subtitle">{$strings.landing.subtitle}</p>
        <div class="hero-actions">
          <button class="cta-primary" onclick={handleLogin}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            {$strings.landing.cta}
          </button>
          <span class="hero-note">{$strings.landing.note}</span>
        </div>
      </div>

      <!-- Canvas mockup -->
      <div class="hero-canvas">
        <div class="canvas-surface">
          <div class="canvas-dots"></div>

          <div class="fact-card card-q" style="--delay: 0s">
            <div class="card-stripe" style="background: var(--color-card-fact)"></div>
            <span class="card-type" style="color: var(--color-card-fact)">fact</span>
            <p class="card-body">{$strings.landing.samples[0]}</p>
          </div>
          <div class="fact-card card-f" style="--delay: 0.15s">
            <div class="card-stripe" style="background: var(--color-card-pain)"></div>
            <span class="card-type" style="color: var(--color-card-pain)">pain</span>
            <p class="card-body">{$strings.landing.samples[1]}</p>
          </div>
          <div class="fact-card card-r" style="--delay: 0.3s">
            <div class="card-stripe" style="background: var(--color-card-question)"></div>
            <span class="card-type" style="color: var(--color-card-question)">question</span>
            <p class="card-body">{$strings.landing.samples[2]}</p>
          </div>
          <div class="fact-card card-h" style="--delay: 0.45s">
            <div class="card-stripe" style="background: var(--color-card-resource)"></div>
            <span class="card-type" style="color: var(--color-card-resource)">resource</span>
            <p class="card-body">{$strings.landing.samples[3]}</p>
          </div>

          <!-- AI question bubble -->
          <div class="ai-bubble">
            <div class="ai-bubble-inner">
              <svg class="ai-bubble-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><circle cx="12" cy="17" r="0.5"/>
              </svg>
              <span class="ai-bubble-text">{$strings.landing.aiBubble}</span>
            </div>
            <div class="ai-bubble-tail"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ METRICS BAR ============ -->
  <section class="metrics-bar">
    <div class="metrics-inner">
      {#each $strings.landing.metrics as m}
        <div class="metric-item">
          <span class="metric-number">{m.metric}</span>
          <span class="metric-label">{m.label}</span>
        </div>
      {/each}
    </div>
  </section>

  <!-- ============ HOW IT WORKS ============ -->
  <section class="how-section">
    <div class="how-inner">
      <div class="section-header">
        <span class="section-kicker">{$strings.landing.howTitle}</span>
        <div class="section-line"></div>
      </div>

      <div class="steps-timeline">
        {#each $strings.landing.steps as step, i}
          <div class="step" style="--i: {i}">
            <div class="step-marker">
              <span class="step-num">{i + 1}</span>
              {#if i < 2}
                <div class="step-connector"></div>
              {/if}
            </div>
            <div class="step-content">
              <h3 class="step-title">{step.title}</h3>
              <p class="step-desc">{step.desc}</p>
            </div>
            <div class="step-visual step-visual-{i}">
              {#if i === 0}
                <div class="sv-scatter">
                  <div class="sv-blob sv-b1">fact</div>
                  <div class="sv-blob sv-b2">fear</div>
                  <div class="sv-blob sv-b3">hope</div>
                  <div class="sv-arrow">→</div>
                  <div class="sv-card-mini">
                    <div class="sv-card-bar" style="background: var(--color-card-fact)"></div>
                  </div>
                </div>
              {:else if i === 1}
                <div class="sv-canvas-mini">
                  <div class="sv-dot" style="--x:20%;--y:30%; background: var(--color-card-question)"></div>
                  <div class="sv-dot" style="--x:60%;--y:20%; background: var(--color-card-fact)"></div>
                  <div class="sv-dot" style="--x:45%;--y:65%; background: var(--color-card-resource)"></div>
                  <div class="sv-dot" style="--x:75%;--y:55%; background: var(--color-card-pain)"></div>
                  <svg class="sv-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
                    <line x1="22" y1="32" x2="58" y2="22" stroke="var(--color-warm-400)" stroke-width="0.8" opacity="0.6"/>
                    <line x1="47" y1="67" x2="22" y2="32" stroke="var(--color-warm-400)" stroke-width="0.8" opacity="0.6"/>
                    <line x1="47" y1="67" x2="73" y2="57" stroke="var(--color-warm-400)" stroke-width="0.8" opacity="0.6"/>
                  </svg>
                </div>
              {:else}
                <div class="sv-blindspot">
                  <div class="sv-pulse"></div>
                  <span class="sv-q">?</span>
                </div>
              {/if}
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ BEFORE / AFTER ============ -->
  <section class="before-after-section">
    <div class="before-after-inner">
      <div class="ba-card ba-before">
        <div class="ba-icon">
          <svg class="ba-svg ba-svg-before" width="40" height="40" viewBox="0 0 40 40" fill="none">
            <circle cx="20" cy="20" r="18" stroke="var(--color-card-pain)" stroke-width="2" stroke-dasharray="4 3" opacity="0.5">
              <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="8s" repeatCount="indefinite"/>
            </circle>
            <path d="M12 16 Q16 10 20 16 Q24 22 28 16" stroke="var(--color-card-pain)" stroke-width="2" stroke-linecap="round" fill="none">
              <animate attributeName="d" values="M12 16 Q16 10 20 16 Q24 22 28 16;M12 18 Q16 24 20 18 Q24 12 28 18;M12 16 Q16 10 20 16 Q24 22 28 16" dur="3s" repeatCount="indefinite"/>
            </path>
            <path d="M12 24 Q16 18 20 24 Q24 30 28 24" stroke="var(--color-card-pain)" stroke-width="2" stroke-linecap="round" fill="none" opacity="0.5">
              <animate attributeName="d" values="M12 24 Q16 18 20 24 Q24 30 28 24;M12 22 Q16 28 20 22 Q24 16 28 22;M12 24 Q16 18 20 24 Q24 30 28 24" dur="3s" repeatCount="indefinite" begin="0.5s"/>
            </path>
          </svg>
        </div>
        <h3 class="ba-title">{$strings.landing.beforeTitle}</h3>
        <ul class="ba-list">
          {#each $strings.landing.beforePoints as point}
            <li class="ba-item ba-item-before">
              <svg class="ba-x" width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="var(--color-card-pain)" stroke-width="2.5" stroke-linecap="round"><line x1="3" y1="3" x2="11" y2="11"/><line x1="11" y1="3" x2="3" y2="11"/></svg>
              {point}
            </li>
          {/each}
        </ul>
      </div>
      <div class="ba-arrow">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-warm-400)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
      </div>
      <div class="ba-card ba-after">
        <div class="ba-icon">
          <svg class="ba-svg ba-svg-after" width="40" height="40" viewBox="0 0 40 40" fill="none">
            <circle cx="20" cy="20" r="16" stroke="var(--color-card-resource)" stroke-width="2" opacity="0.3"/>
            <circle cx="20" cy="20" r="16" stroke="var(--color-card-resource)" stroke-width="2" stroke-dasharray="100.5" stroke-dashoffset="100.5" stroke-linecap="round">
              <animate attributeName="stroke-dashoffset" from="100.5" to="0" dur="2s" fill="freeze" begin="0.5s"/>
            </circle>
            <path d="M14 20l4 4 8-8" stroke="var(--color-card-resource)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="24" stroke-dashoffset="24">
              <animate attributeName="stroke-dashoffset" from="24" to="0" dur="0.6s" fill="freeze" begin="1.8s"/>
            </path>
          </svg>
        </div>
        <h3 class="ba-title">{$strings.landing.afterTitle}</h3>
        <ul class="ba-list">
          {#each $strings.landing.afterPoints as point}
            <li class="ba-item ba-item-after">
              <svg class="ba-check" width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="var(--color-card-resource)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="2.5 7.5 5.5 10.5 11.5 4"/></svg>
              {point}
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </section>

  <!-- ============ FEATURES ============ -->
  <section class="features-section">
    <div class="features-inner">
      <div class="section-header">
        <span class="section-kicker">{$strings.landing.featuresTitle}</span>
        <div class="section-line"></div>
      </div>
      <div class="features-grid">
        {#each $strings.landing.features as feature, i}
          <div class="feature-card">
            <div class="feature-icon">
              {#if i === 0}
                <!-- Voice / Microphone -->
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                  <rect x="11" y="4" width="10" height="16" rx="5" stroke="var(--color-warm-700)" stroke-width="2"/>
                  <path d="M7 16a9 9 0 0 0 18 0" stroke="var(--color-warm-500)" stroke-width="2" stroke-linecap="round"/>
                  <line x1="16" y1="25" x2="16" y2="28" stroke="var(--color-warm-500)" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="16" cy="12" r="2" fill="var(--color-card-pain)" class="mic-pulse">
                    <animate attributeName="r" values="1.5;3;1.5" dur="1.5s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="1;0.4;1" dur="1.5s" repeatCount="indefinite"/>
                  </circle>
                </svg>
              {:else if i === 1}
                <!-- Canvas / Grid -->
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                  <rect x="3" y="3" width="26" height="26" rx="4" stroke="var(--color-warm-700)" stroke-width="2"/>
                  <rect x="7" y="7" width="7" height="5" rx="1.5" fill="var(--color-card-fact)" opacity="0.7"/>
                  <rect x="18" y="8" width="7" height="5" rx="1.5" fill="var(--color-card-pain)" opacity="0.7"/>
                  <rect x="9" y="16" width="7" height="5" rx="1.5" fill="var(--color-card-question)" opacity="0.7"/>
                  <rect x="19" y="19" width="6" height="5" rx="1.5" fill="var(--color-card-resource)" opacity="0.7"/>
                </svg>
              {:else if i === 2}
                <!-- Compass / Path -->
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                  <circle cx="16" cy="16" r="13" stroke="var(--color-warm-700)" stroke-width="2"/>
                  <circle cx="16" cy="16" r="2" fill="var(--color-warm-700)"/>
                  <polygon points="16,5 18.5,14 16,12 13.5,14" fill="var(--color-card-pain)" opacity="0.8"/>
                  <polygon points="16,27 13.5,18 16,20 18.5,18" fill="var(--color-warm-500)" opacity="0.6"/>
                  <line x1="16" y1="1" x2="16" y2="5" stroke="var(--color-warm-400)" stroke-width="1.5" stroke-linecap="round"/>
                  <line x1="16" y1="27" x2="16" y2="31" stroke="var(--color-warm-400)" stroke-width="1.5" stroke-linecap="round"/>
                  <line x1="1" y1="16" x2="5" y2="16" stroke="var(--color-warm-400)" stroke-width="1.5" stroke-linecap="round"/>
                  <line x1="27" y1="16" x2="31" y2="16" stroke="var(--color-warm-400)" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              {:else}
                <!-- Lightbulb / Blind spots -->
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                  <path d="M16 4a9 9 0 0 0-5 16.5V24a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-3.5A9 9 0 0 0 16 4z" stroke="var(--color-warm-700)" stroke-width="2"/>
                  <line x1="13" y1="28" x2="19" y2="28" stroke="var(--color-warm-500)" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="16" cy="12" r="0" fill="var(--color-card-hypothesis)" opacity="0.6">
                    <animate attributeName="r" values="0;5;0" dur="3s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0;0.5;0" dur="3s" repeatCount="indefinite"/>
                  </circle>
                  <line x1="16" y1="3" x2="16" y2="0" stroke="var(--color-card-hypothesis)" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
                  <line x1="25" y1="7" x2="27" y2="5" stroke="var(--color-card-hypothesis)" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
                  <line x1="7" y1="7" x2="5" y2="5" stroke="var(--color-card-hypothesis)" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
                </svg>
              {/if}
            </div>
            <h3 class="feature-title">{feature.title}</h3>
            <p class="feature-desc">{feature.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ PERSONAS ============ -->
  <section class="personas-section">
    <div class="personas-inner">
      <div class="section-header">
        <span class="section-kicker">{$strings.landing.personasTitle}</span>
        <div class="section-line"></div>
      </div>
      <div class="personas-grid">
        {#each $strings.landing.personas as persona, i}
          <div class="persona-card">
            <div class="persona-icon">
              {#if i === 0}
                <!-- Crossroads / Signpost -->
                <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                  <line x1="18" y1="6" x2="18" y2="32" stroke="var(--color-warm-600)" stroke-width="2.5" stroke-linecap="round"/>
                  <path d="M8 11h14l3 3-3 3H8z" fill="var(--color-card-fact)" opacity="0.6" stroke="var(--color-card-fact)" stroke-width="1"/>
                  <path d="M28 20H14l-3 3 3 3h14z" fill="var(--color-card-hypothesis)" opacity="0.6" stroke="var(--color-card-hypothesis)" stroke-width="1"/>
                </svg>
              {:else if i === 1}
                <!-- Rocket -->
                <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                  <path d="M18 4c-4 6-5 14-3 20h6c2-6 1-14-3-20z" stroke="var(--color-warm-600)" stroke-width="2" fill="none"/>
                  <circle cx="18" cy="16" r="2.5" fill="var(--color-card-pain)" opacity="0.6"/>
                  <path d="M15 24l-4 4 3-1" stroke="var(--color-warm-500)" stroke-width="1.5" stroke-linecap="round" fill="none"/>
                  <path d="M21 24l4 4-3-1" stroke="var(--color-warm-500)" stroke-width="1.5" stroke-linecap="round" fill="none"/>
                  <path d="M16 29q2 4 4 0" stroke="var(--color-card-hypothesis)" stroke-width="1.5" stroke-linecap="round" fill="none" opacity="0.7">
                    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="1s" repeatCount="indefinite"/>
                  </path>
                </svg>
              {:else if i === 2}
                <!-- Heart -->
                <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                  <path d="M18 30 C8 22 4 16 4 11a6 6 0 0 1 6-6c3 0 5.5 1.5 8 5 2.5-3.5 5-5 8-5a6 6 0 0 1 6 6c0 5-4 11-14 19z" stroke="var(--color-card-pain)" stroke-width="2" fill="var(--color-card-pain)" fill-opacity="0.12">
                    <animate attributeName="fill-opacity" values="0.08;0.2;0.08" dur="2s" repeatCount="indefinite"/>
                  </path>
                </svg>
              {:else}
                <!-- Map / Navigation -->
                <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                  <path d="M4 8l10-4 8 4 10-4v22l-10 4-8-4-10 4z" stroke="var(--color-warm-600)" stroke-width="2" fill="none"/>
                  <line x1="14" y1="4" x2="14" y2="26" stroke="var(--color-warm-400)" stroke-width="1.5"/>
                  <line x1="22" y1="8" x2="22" y2="30" stroke="var(--color-warm-400)" stroke-width="1.5"/>
                  <circle cx="18" cy="17" r="3" fill="var(--color-card-question)" opacity="0.5">
                    <animate attributeName="r" values="2.5;3.5;2.5" dur="2.5s" repeatCount="indefinite"/>
                  </circle>
                </svg>
              {/if}
            </div>
            <h3 class="persona-title">{persona.title}</h3>
            <p class="persona-desc">{persona.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ METHODOLOGY ============ -->
  <section class="methodology-section">
    <div class="methodology-inner">
      <div class="methodology-card">
        <div class="methodology-icon">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
            <path d="M24 6c-8 0-14 6-14 13 0 5 3 9 7 11v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4c4-2 7-6 7-11 0-7-6-13-14-13z" stroke="var(--color-warm-600)" stroke-width="2" fill="none"/>
            <path d="M18 38h12" stroke="var(--color-warm-500)" stroke-width="2" stroke-linecap="round"/>
            <path d="M20 42h8" stroke="var(--color-warm-400)" stroke-width="2" stroke-linecap="round"/>
            <path d="M17 17c0-4 3-7 7-7" stroke="var(--color-warm-400)" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            <!-- Neural connections -->
            <circle cx="20" cy="16" r="1.5" fill="var(--color-card-fact)" opacity="0.6">
              <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="28" cy="14" r="1.5" fill="var(--color-card-question)" opacity="0.6">
              <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite" begin="0.7s"/>
            </circle>
            <circle cx="24" cy="20" r="1.5" fill="var(--color-card-resource)" opacity="0.6">
              <animate attributeName="opacity" values="0.3;0.8;0.3" dur="2s" repeatCount="indefinite" begin="1.3s"/>
            </circle>
            <line x1="20" y1="16" x2="28" y2="14" stroke="var(--color-warm-400)" stroke-width="0.8" opacity="0.3"/>
            <line x1="20" y1="16" x2="24" y2="20" stroke="var(--color-warm-400)" stroke-width="0.8" opacity="0.3"/>
            <line x1="28" y1="14" x2="24" y2="20" stroke="var(--color-warm-400)" stroke-width="0.8" opacity="0.3"/>
          </svg>
        </div>
        <h2 class="methodology-title">{$strings.landing.methodologyTitle}</h2>
        <p class="methodology-text">{$strings.landing.methodologyText}</p>
      </div>
    </div>
  </section>

  <!-- ============ RESULT ============ -->
  <section class="result-section">
    <div class="result-inner">
      <div class="result-card">
        <h2 class="result-title">{$strings.landing.resultTitle}</h2>
        <p class="result-text">{$strings.landing.resultText}</p>
        <div class="result-pills">
          {#each $strings.landing.resultItems as item}
            <div class="result-pill">
              <span class="pill-check">&#10003;</span>
              {item}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="faq-section">
    <div class="faq-inner">
      <div class="section-header">
        <span class="section-kicker">{$strings.landing.faqTitle}</span>
        <div class="section-line"></div>
      </div>
      <div class="faq-list">
        {#each $strings.landing.faq as item, i}
          <div class="faq-item" class:open={openFaqIndex === i}>
            <button class="faq-question" onclick={() => toggleFaq(i)}>
              <span>{item.q}</span>
              <svg class="faq-chevron" class:faq-chevron-open={openFaqIndex === i} width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                <line x1="4" y1="10" x2="16" y2="10"/>
                <line class="faq-chevron-vert" x1="10" y1="4" x2="10" y2="16"/>
              </svg>
            </button>
            {#if openFaqIndex === i}
              <div class="faq-answer">
                <p>{item.a}</p>
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ FINAL CTA ============ -->
  <footer class="footer-cta">
    <div class="footer-bg">
      <div class="footer-orb footer-orb-1"></div>
      <div class="footer-orb footer-orb-2"></div>
    </div>
    <div class="footer-inner">
      <h2 class="footer-title">{$strings.landing.ctaRepeat}</h2>
      <button class="cta-light" onclick={handleLogin}>
        {$strings.landing.cta}
      </button>
      <p class="footer-note">{$strings.landing.note}</p>
    </div>
  </footer>
</div>

<style>
  /* ============================
     GLOBAL OVERRIDES
     ============================ */
  :global(html.landing-active, body.landing-active) {
    height: auto !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    -webkit-overflow-scrolling: touch;
  }
  :global(body.landing-active #app) {
    min-height: 100%;
    height: auto;
  }

  /* ============================
     ROOT
     ============================ */
  .landing-root {
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
    width: 100%;
    min-height: 100vh;
    background: #f8f1e7;
    color: var(--color-warm-800);
    overflow-x: hidden;
  }

  /* ============================
     NAV
     ============================ */
  .nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 32px;
    background: rgba(248, 241, 231, 0.7);
    backdrop-filter: blur(20px) saturate(1.4);
    border-bottom: 1px solid rgba(154, 107, 63, 0.08);
  }

  .nav-logo {
    font-family: var(--font-accent);
    font-size: 1.6rem;
    color: var(--color-warm-500);
    letter-spacing: 0.02em;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .lang-toggle {
    display: flex;
    gap: 2px;
    padding: 3px;
    border-radius: 10px;
    background: rgba(154, 107, 63, 0.08);
  }

  .lang-btn {
    padding: 5px 12px;
    font-family: var(--font-body);
    font-size: 12px;
    font-weight: 700;
    border: none;
    border-radius: 7px;
    background: transparent;
    color: var(--color-warm-600);
    transition: all 0.2s var(--ease-out);
  }

  .lang-btn.active {
    background: white;
    color: var(--color-warm-800);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }

  .nav-cta {
    display: none;
    padding: 8px 20px;
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 600;
    border: 1.5px solid var(--color-warm-800);
    border-radius: 100px;
    background: transparent;
    color: var(--color-warm-800);
    transition: all 0.25s var(--ease-out);
  }

  .nav-cta:hover {
    background: var(--color-warm-800);
    color: #faf3e8;
  }

  @media (min-width: 768px) {
    .nav-cta { display: inline-flex; }
  }

  /* ============================
     HERO
     ============================ */
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 100px 32px 60px;
    overflow: hidden;
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .hero-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
  }
  .hero-orb-1 {
    width: 600px; height: 600px;
    top: -15%; left: -10%;
    background: radial-gradient(circle, rgba(212, 165, 116, 0.4) 0%, transparent 70%);
  }
  .hero-orb-2 {
    width: 500px; height: 500px;
    top: 10%; right: -5%;
    background: radial-gradient(circle, rgba(149, 117, 205, 0.12) 0%, transparent 70%);
  }
  .hero-orb-3 {
    width: 300px; height: 300px;
    bottom: 5%; left: 30%;
    background: radial-gradient(circle, rgba(129, 199, 132, 0.1) 0%, transparent 70%);
  }

  .hero-grain {
    position: absolute;
    inset: 0;
    opacity: 0.3;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    background-size: 200px;
  }

  .hero-inner {
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
    gap: 48px;
    align-items: center;
  }

  @media (min-width: 1024px) {
    .hero-inner { grid-template-columns: 1fr 1.1fr; gap: 64px; }
  }

  .hero-copy {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    align-self: flex-start;
    padding: 6px 16px 6px 10px;
    background: rgba(154, 107, 63, 0.08);
    border: 1px solid rgba(154, 107, 63, 0.15);
    border-radius: 100px;
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 500;
    color: var(--color-warm-600);
    letter-spacing: 0.02em;
  }

  .hero-badge-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--color-card-resource);
    box-shadow: 0 0 8px rgba(129, 199, 132, 0.5);
    animation: pulse-dot 2s ease-in-out infinite;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.3); }
  }

  .hero-title {
    font-family: var(--font-display);
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 700;
    line-height: 1.08;
    letter-spacing: -0.02em;
    color: var(--color-warm-800);
  }

  .hero-subtitle {
    font-family: var(--font-body);
    font-size: clamp(1rem, 1.8vw, 1.15rem);
    line-height: 1.65;
    color: var(--color-warm-700);
    max-width: 480px;
  }

  .hero-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 16px;
    margin-top: 8px;
  }

  .cta-primary {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 14px 28px;
    font-family: var(--font-body);
    font-size: 15px;
    font-weight: 600;
    border: none;
    border-radius: 14px;
    background: var(--color-warm-800);
    color: #faf3e8;
    box-shadow:
      0 1px 0 0 rgba(255, 255, 255, 0.06) inset,
      0 12px 28px -4px rgba(47, 42, 36, 0.35),
      0 4px 10px -2px rgba(47, 42, 36, 0.2);
    transition: all 0.3s var(--ease-out);
  }

  .cta-primary:hover {
    transform: translateY(-2px);
    box-shadow:
      0 1px 0 0 rgba(255, 255, 255, 0.06) inset,
      0 18px 36px -6px rgba(47, 42, 36, 0.4),
      0 6px 14px -3px rgba(47, 42, 36, 0.25);
  }

  .hero-note {
    font-family: var(--font-body);
    font-size: 13px;
    color: var(--color-warm-500);
  }

  /* ============================
     HERO CANVAS MOCKUP
     ============================ */
  .hero-canvas { position: relative; display: flex; justify-content: center; }

  .canvas-surface {
    position: relative;
    width: 100%; max-width: 480px; height: 420px;
    background: rgba(255, 253, 248, 0.6);
    border: 1px solid rgba(154, 107, 63, 0.12);
    border-radius: 20px;
    box-shadow:
      0 40px 80px -20px rgba(47, 42, 36, 0.15),
      0 16px 32px -8px rgba(47, 42, 36, 0.08),
      0 0 0 1px rgba(255, 255, 255, 0.6) inset;
    overflow: hidden;
  }

  .canvas-dots {
    position: absolute; inset: 0;
    background-image: radial-gradient(circle, rgba(154, 107, 63, 0.12) 1px, transparent 1px);
    background-size: 24px 24px;
  }

  .canvas-lines {
    position: absolute; inset: 0;
    width: 100%; height: 100%; z-index: 1;
  }

  .canvas-lines path {
    animation: draw-line 2s ease-out forwards;
    stroke-dasharray: 200; stroke-dashoffset: 200;
  }

  @keyframes draw-line { to { stroke-dashoffset: 0; } }

  .fact-card {
    position: absolute; z-index: 2;
    padding: 14px 16px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 24px -4px rgba(47, 42, 36, 0.12), 0 2px 6px -1px rgba(47, 42, 36, 0.06);
    font-family: var(--font-body);
    max-width: 200px;
    animation: card-appear 0.6s var(--ease-spring) calc(var(--delay) + 0.3s) both;
    transition: transform 0.3s var(--ease-out), box-shadow 0.3s var(--ease-out);
  }

  .fact-card:hover {
    transform: translate(0, -4px) rotate(var(--r, 0deg)) scale(1.04);
    box-shadow: 0 14px 36px -6px rgba(47, 42, 36, 0.18), 0 4px 10px -2px rgba(47, 42, 36, 0.08);
    z-index: 10;
  }

  @keyframes card-appear {
    from { opacity: 0; transform: translate(0, 20px) rotate(var(--r, 0deg)) scale(0.85); }
    to { opacity: 1; transform: translate(0, 0) rotate(var(--r, 0deg)) scale(1); }
  }

  .card-stripe { height: 4px; border-radius: 4px; margin-bottom: 10px; }
  .card-type { display: block; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
  .card-body { font-size: 13px; line-height: 1.4; color: var(--color-warm-700); }

  .card-q { --r: -5deg; top: 8%; left: 8%; width: 190px; }
  .card-f { --r: 3deg; top: 12%; right: 6%; width: 185px; }
  .card-r { --r: -2deg; bottom: 26%; left: 12%; width: 175px; }
  .card-h { --r: 4deg; bottom: 8%; right: 10%; width: 170px; }

  .ai-bubble {
    position: absolute; bottom: 36%; left: 44%; z-index: 20;
    animation: bubble-appear 0.5s var(--ease-spring) 1s both;
  }

  .ai-bubble-inner {
    display: flex; align-items: center; gap: 6px;
    padding: 8px 14px;
    background: var(--color-warm-800);
    color: #faf3e8;
    border-radius: 12px 12px 12px 4px;
    font-family: var(--font-body);
    font-size: 11px; font-weight: 500;
    box-shadow: 0 6px 20px -4px rgba(47, 42, 36, 0.25);
    white-space: nowrap;
  }

  .ai-bubble-icon { opacity: 0.7; flex-shrink: 0; }

  .ai-bubble-tail {
    width: 8px; height: 8px;
    background: var(--color-warm-800);
    transform: rotate(45deg);
    position: absolute; bottom: -3px; left: 8px;
  }

  @keyframes bubble-appear {
    from { opacity: 0; transform: scale(0.8) translateY(8px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
  }

  /* ============================
     METRICS BAR
     ============================ */
  .metrics-bar {
    background: var(--color-warm-800);
    padding: 32px;
  }

  .metrics-inner {
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
    text-align: center;
  }

  @media (min-width: 768px) {
    .metrics-inner { grid-template-columns: repeat(4, 1fr); }
  }

  .metric-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .metric-number {
    font-family: var(--font-display);
    font-size: clamp(1.6rem, 3vw, 2.2rem);
    font-weight: 700;
    color: var(--color-warm-100);
  }

  .metric-label {
    font-family: var(--font-body);
    font-size: 13px;
    color: var(--color-warm-400);
    letter-spacing: 0.02em;
  }

  /* ============================
     HOW IT WORKS
     ============================ */
  .how-section {
    position: relative;
    padding: 80px 32px;
    background: linear-gradient(180deg, #f8f1e7 0%, #f3ead9 100%);
  }

  .how-inner { max-width: 960px; margin: 0 auto; }

  .section-header {
    display: flex; align-items: center; gap: 20px;
    margin-bottom: 56px;
  }

  .section-kicker {
    font-family: var(--font-body);
    font-size: 13px; font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--color-warm-500);
    white-space: nowrap;
  }

  .section-line {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--color-warm-400) 0%, transparent 100%);
    opacity: 0.3;
  }

  .steps-timeline { display: flex; flex-direction: column; }

  .step {
    display: grid;
    grid-template-columns: 48px 1fr;
    gap: 24px; padding: 32px 0;
    border-bottom: 1px solid rgba(154, 107, 63, 0.1);
    position: relative;
  }

  .step:last-child { border-bottom: none; }

  @media (min-width: 768px) {
    .step { grid-template-columns: 48px 1fr 180px; align-items: start; }
  }

  .step-marker { position: relative; display: flex; flex-direction: column; align-items: center; }

  .step-num {
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 12px;
    background: var(--color-warm-800);
    color: #faf3e8;
    font-family: var(--font-display);
    font-size: 16px; font-weight: 700;
  }

  .step-connector {
    width: 1.5px; flex: 1; min-height: 40px;
    background: linear-gradient(180deg, var(--color-warm-800) 0%, var(--color-warm-300) 100%);
    margin-top: 8px;
  }

  .step-content { padding-top: 6px; }

  .step-title {
    font-family: var(--font-display);
    font-size: 1.3rem; font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 10px;
  }

  .step-desc {
    font-family: var(--font-body);
    font-size: 0.95rem; line-height: 1.7;
    color: var(--color-warm-600);
    max-width: 480px;
  }

  .step-visual {
    display: none; align-items: center; justify-content: center; height: 100px;
  }

  @media (min-width: 768px) {
    .step-visual { display: flex; }
  }

  .sv-scatter { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; justify-content: center; }

  .sv-blob {
    padding: 4px 10px;
    background: rgba(154, 107, 63, 0.08);
    border: 1px dashed rgba(154, 107, 63, 0.2);
    border-radius: 8px;
    font-family: var(--font-body);
    font-size: 11px; color: var(--color-warm-600);
    animation: wobble 3s ease-in-out infinite alternate;
  }
  .sv-b1 { animation-delay: 0s; }
  .sv-b2 { animation-delay: 0.3s; }
  .sv-b3 { animation-delay: 0.6s; }

  @keyframes wobble {
    0% { transform: translateY(0) rotate(0deg); }
    100% { transform: translateY(-3px) rotate(2deg); }
  }

  .sv-arrow { font-size: 18px; color: var(--color-warm-400); margin: 0 4px; }

  .sv-card-mini {
    width: 40px; height: 48px;
    background: white; border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    padding: 6px;
  }
  .sv-card-bar { height: 3px; border-radius: 3px; }

  .sv-canvas-mini {
    position: relative; width: 120px; height: 80px;
    background: rgba(255, 253, 248, 0.8);
    border: 1px solid rgba(154, 107, 63, 0.15);
    border-radius: 8px;
  }

  .sv-dot {
    position: absolute; width: 10px; height: 10px;
    border-radius: 50%;
    top: var(--y); left: var(--x);
    transform: translate(-50%, -50%);
  }

  .sv-lines { position: absolute; inset: 0; width: 100%; height: 100%; }

  .sv-blindspot {
    position: relative; width: 56px; height: 56px;
    display: flex; align-items: center; justify-content: center;
  }

  .sv-pulse {
    position: absolute; inset: 0;
    border-radius: 50%;
    border: 2px dashed var(--color-warm-400);
    animation: pulse-ring 2.5s ease-in-out infinite;
  }

  @keyframes pulse-ring {
    0%, 100% { transform: scale(1); opacity: 0.6; }
    50% { transform: scale(1.25); opacity: 0.2; }
  }

  .sv-q {
    font-family: var(--font-display);
    font-size: 24px; font-weight: 700;
    color: var(--color-warm-500);
  }

  /* ============================
     BEFORE / AFTER
     ============================ */
  .before-after-section {
    padding: 80px 32px;
    background: #f3ead9;
  }

  .before-after-inner {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
  }

  @media (min-width: 768px) {
    .before-after-inner {
      flex-direction: row;
      align-items: stretch;
      gap: 32px;
    }
  }

  .ba-card {
    flex: 1;
    padding: 36px 32px;
    border-radius: 20px;
    font-family: var(--font-body);
  }

  .ba-before {
    background: rgba(229, 115, 115, 0.06);
    border: 1px solid rgba(229, 115, 115, 0.15);
  }

  .ba-after {
    background: rgba(129, 199, 132, 0.06);
    border: 1px solid rgba(129, 199, 132, 0.15);
  }

  .ba-icon {
    margin-bottom: 16px;
    display: flex;
    align-items: center;
  }

  .ba-title {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 20px;
  }

  .ba-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .ba-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--color-warm-700);
  }

  .ba-x, .ba-check {
    flex-shrink: 0;
    margin-top: 3px;
  }

  .ba-arrow {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  @media (max-width: 767px) {
    .ba-arrow { transform: rotate(90deg); }
  }

  /* ============================
     FEATURES
     ============================ */
  .features-section {
    padding: 80px 32px;
    background: #f8f1e7;
  }

  .features-inner { max-width: 960px; margin: 0 auto; }

  .features-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }

  @media (min-width: 768px) {
    .features-grid { grid-template-columns: repeat(2, 1fr); }
  }

  .feature-card {
    padding: 32px 28px;
    background: white;
    border-radius: 20px;
    border: 1px solid rgba(154, 107, 63, 0.08);
    box-shadow: 0 4px 16px -4px rgba(47, 42, 36, 0.06);
    transition: transform 0.3s var(--ease-out), box-shadow 0.3s var(--ease-out);
  }

  .feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px -8px rgba(47, 42, 36, 0.12);
  }

  .feature-icon {
    width: 56px; height: 56px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(154, 107, 63, 0.06);
    border-radius: 14px;
    margin-bottom: 16px;
  }

  .feature-title {
    font-family: var(--font-display);
    font-size: 1.15rem; font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 8px;
  }

  .feature-desc {
    font-family: var(--font-body);
    font-size: 0.95rem; line-height: 1.6;
    color: var(--color-warm-600);
  }

  /* ============================
     PERSONAS
     ============================ */
  .personas-section {
    padding: 80px 32px;
    background: linear-gradient(180deg, #f8f1e7 0%, #f3ead9 100%);
  }

  .personas-inner { max-width: 960px; margin: 0 auto; }

  .personas-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
  }

  @media (min-width: 640px) {
    .personas-grid { grid-template-columns: repeat(2, 1fr); }
  }

  @media (min-width: 1024px) {
    .personas-grid { grid-template-columns: repeat(4, 1fr); }
  }

  .persona-card {
    padding: 28px 24px;
    background: white;
    border-radius: 16px;
    border: 1px solid rgba(154, 107, 63, 0.08);
    text-align: center;
    transition: transform 0.3s var(--ease-out);
  }

  .persona-card:hover { transform: translateY(-4px); }

  .persona-icon {
    width: 52px; height: 52px;
    display: flex; align-items: center; justify-content: center;
    background: rgba(154, 107, 63, 0.05);
    border-radius: 50%;
    margin: 0 auto 14px;
  }

  .persona-title {
    font-family: var(--font-display);
    font-size: 1.05rem; font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 8px;
  }

  .persona-desc {
    font-family: var(--font-body);
    font-size: 0.9rem; line-height: 1.5;
    color: var(--color-warm-600);
  }

  /* ============================
     METHODOLOGY
     ============================ */
  .methodology-section {
    padding: 64px 32px;
    background: #f3ead9;
  }

  .methodology-inner { max-width: 720px; margin: 0 auto; }

  .methodology-card {
    text-align: center;
    padding: 48px 40px;
    background: white;
    border-radius: 24px;
    border: 1px solid rgba(154, 107, 63, 0.08);
    box-shadow: 0 8px 24px -8px rgba(47, 42, 36, 0.08);
  }

  .methodology-icon { margin-bottom: 20px; display: flex; justify-content: center; }

  .methodology-title {
    font-family: var(--font-display);
    font-size: clamp(1.4rem, 2.5vw, 1.8rem);
    font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 16px;
  }

  .methodology-text {
    font-family: var(--font-body);
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--color-warm-600);
    max-width: 560px;
    margin: 0 auto;
  }

  /* ============================
     RESULT
     ============================ */
  .result-section {
    padding: 80px 32px;
    background: #f8f1e7;
  }

  .result-inner { max-width: 800px; margin: 0 auto; }

  .result-card {
    position: relative;
    padding: 48px 40px;
    background: white;
    border-radius: 24px;
    box-shadow: 0 32px 64px -16px rgba(47, 42, 36, 0.1), 0 0 0 1px rgba(154, 107, 63, 0.06);
    overflow: hidden;
  }

  .result-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, var(--color-card-question), var(--color-card-fact), var(--color-card-resource), var(--color-card-hypothesis), var(--color-card-pain));
  }

  .result-title {
    font-family: var(--font-display);
    font-size: clamp(1.6rem, 3vw, 2.2rem);
    font-weight: 700; color: var(--color-warm-800);
    margin-bottom: 16px;
  }

  .result-text {
    font-family: var(--font-body);
    font-size: 1.05rem; line-height: 1.7;
    color: var(--color-warm-600);
    margin-bottom: 32px; max-width: 560px;
  }

  .result-pills { display: flex; flex-wrap: wrap; gap: 12px; }

  .result-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 16px;
    background: var(--color-warm-100);
    border-radius: 100px;
    font-family: var(--font-body);
    font-size: 14px; color: var(--color-warm-700);
  }

  .pill-check { color: var(--color-card-resource); font-weight: 700; font-size: 13px; }

  /* ============================
     FAQ
     ============================ */
  .faq-section {
    padding: 80px 32px;
    background: linear-gradient(180deg, #f8f1e7 0%, #f3ead9 100%);
  }

  .faq-inner { max-width: 720px; margin: 0 auto; }

  .faq-list { display: flex; flex-direction: column; gap: 0; }

  .faq-item {
    border-bottom: 1px solid rgba(154, 107, 63, 0.12);
  }

  .faq-question {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding: 20px 0;
    background: none;
    border: none;
    font-family: var(--font-body);
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-warm-800);
    text-align: left;
    transition: color 0.2s;
  }

  .faq-question:hover { color: var(--color-warm-500); }

  .faq-chevron {
    color: var(--color-warm-400);
    flex-shrink: 0;
    transition: transform 0.3s var(--ease-out);
  }

  .faq-chevron-open { transform: rotate(90deg); }

  .faq-chevron-vert {
    transition: transform 0.3s var(--ease-out), opacity 0.2s;
    transform-origin: center;
  }

  .faq-chevron-open .faq-chevron-vert {
    opacity: 0;
    transform: rotate(90deg);
  }

  .faq-answer {
    padding: 0 0 20px;
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.65;
    color: var(--color-warm-600);
    animation: faq-open 0.3s var(--ease-out);
  }

  @keyframes faq-open {
    from { opacity: 0; transform: translateY(-8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* ============================
     FOOTER CTA
     ============================ */
  .footer-cta {
    position: relative;
    padding: 96px 32px;
    background: var(--color-warm-800);
    overflow: hidden;
  }

  .footer-bg { position: absolute; inset: 0; pointer-events: none; }

  .footer-orb { position: absolute; border-radius: 50%; filter: blur(60px); }
  .footer-orb-1 {
    width: 400px; height: 400px; top: -30%; right: -10%;
    background: radial-gradient(circle, rgba(154, 107, 63, 0.2) 0%, transparent 70%);
  }
  .footer-orb-2 {
    width: 300px; height: 300px; bottom: -20%; left: 10%;
    background: radial-gradient(circle, rgba(149, 117, 205, 0.08) 0%, transparent 70%);
  }

  .footer-inner {
    position: relative; max-width: 600px;
    margin: 0 auto; text-align: center;
  }

  .footer-title {
    font-family: var(--font-display);
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 700; color: var(--color-warm-100);
    margin-bottom: 32px; line-height: 1.15;
  }

  .cta-light {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 16px 32px;
    font-family: var(--font-body);
    font-size: 16px; font-weight: 600;
    border: none; border-radius: 14px;
    background: #faf3e8; color: var(--color-warm-800);
    box-shadow:
      0 1px 0 0 rgba(255, 255, 255, 0.2) inset,
      0 12px 28px -4px rgba(0, 0, 0, 0.3);
    transition: all 0.3s var(--ease-out);
  }

  .cta-light:hover {
    transform: translateY(-2px);
    box-shadow:
      0 1px 0 0 rgba(255, 255, 255, 0.2) inset,
      0 18px 40px -6px rgba(0, 0, 0, 0.35);
  }

  .footer-note {
    margin-top: 20px;
    font-family: var(--font-body);
    font-size: 13px;
    color: rgba(250, 243, 232, 0.4);
  }

  /* ============================
     RESPONSIVE
     ============================ */
  @media (max-width: 768px) {
    .nav { padding: 12px 20px; }
    .hero { padding: 90px 20px 40px; }
    .hero-inner { gap: 32px; }
    .canvas-surface { max-width: 360px; height: 340px; }
    .card-q { width: 155px; top: 4%; left: 4%; }
    .card-f { width: 150px; top: 8%; right: 2%; }
    .card-r { width: 140px; bottom: 28%; left: 6%; }
    .card-h { width: 135px; bottom: 6%; right: 4%; }
    .fact-card { padding: 10px 12px; }
    .card-body { font-size: 11px; }
    .card-type { font-size: 9px; }
    .card-stripe { height: 3px; margin-bottom: 6px; }
    .how-section { padding: 60px 20px; }
    .before-after-section { padding: 60px 20px; }
    .features-section { padding: 60px 20px; }
    .personas-section { padding: 60px 20px; }
    .methodology-section { padding: 48px 20px; }
    .methodology-card { padding: 32px 24px; }
    .result-section { padding: 60px 20px; }
    .result-card { padding: 32px 24px; }
    .faq-section { padding: 60px 20px; }
    .footer-cta { padding: 64px 20px; }
    .step { grid-template-columns: 40px 1fr; gap: 16px; padding: 24px 0; }
    .step-num { width: 34px; height: 34px; font-size: 14px; border-radius: 10px; }
  }

  @media (max-width: 420px) {
    .hero-title { font-size: 2rem; }
    .canvas-surface { height: 300px; }
    .card-q { width: 140px; }
    .card-f { width: 135px; }
    .card-r { width: 130px; }
    .card-h { width: 120px; }
  }
</style>
