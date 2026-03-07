<script lang="ts">
  import { onMount } from "svelte";
  import { auth } from "../stores/auth";
  import { strings, locale, setLocale, availableLocales } from "../stores/i18n";
  import type { Locale } from "../stores/i18n";
  import {
    Hexagon,
    Sparkles,
    MapPin,
    EyeOff,
    LayoutTemplate,
    ArrowRight,
    ArrowRightCircle,
    Target,
    Users,
    BookOpen,
    ShieldCheck,
    CloudFog,
    X,
    Sun,
    Check,
    ChevronRight,
    BrainCircuit,
  } from "lucide-svelte";

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
    root.classList.add("landing-active");
    document.body.classList.add("landing-active");
    return () => {
      root.classList.remove("landing-active");
      document.body.classList.remove("landing-active");
    };
  });
</script>

<div class="landing-root">
  <!-- ============ NAV ============ -->
  <nav class="nav">
    <div class="nav-logo">{$strings.landing.kicker}</div>
    <div class="nav-links">
      {#each $strings.landing.navLinks as link}
        <a class="nav-link" href={`#${link.id}`}>{link.label}</a>
      {/each}
    </div>
    <div class="nav-right">
      <div
        class="lang-toggle"
        role="group"
        aria-label={$strings.language.toggleAria}
      >
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
        {$strings.landing.navCta}
      </button>
    </div>
  </nav>

  <!-- ============ HERO ============ -->
  <section class="hero">
    <div class="hero-bg">
      <div class="hero-grid-pattern"></div>
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
            {$strings.landing.cta}
            <ArrowRight size={18} strokeWidth={2.5} />
          </button>
          <span class="hero-note">{$strings.landing.note}</span>
        </div>
      </div>

      <!-- High-Fidelity Floating Card Mockup -->
      <div class="hero-mockup">
        <div class="floating-mockup">
          <div class="fm-card fm-main">
            <div class="fm-header">
              <div
                class="fm-tag"
                style="color: var(--color-card-pain); background: rgba(224, 96, 96, 0.1);"
              >
                <Target size={14} strokeWidth={2.5} />
                {$strings.landing.mockupLabels.pain}
              </div>
            </div>
            <h3 class="fm-title">{$strings.landing.samples[1]}</h3>
            <div class="fm-footer">
              <div class="fm-author"></div>
            </div>
          </div>

          <div class="fm-card fm-sub fm-left">
            <div class="fm-header">
              <div
                class="fm-tag"
                style="color: var(--color-card-question); background: rgba(126, 94, 191, 0.1);"
              >
                <span style="font-weight:bold; font-size:12px;">?</span>
                {$strings.landing.mockupLabels.question}
              </div>
            </div>
            <p class="fm-text">{$strings.landing.samples[2]}</p>
          </div>

          <div class="fm-card fm-sub fm-right">
            <div class="fm-header">
              <div
                class="fm-tag"
                style="color: var(--color-card-resource); background: rgba(102, 181, 106, 0.1);"
              >
                <BookOpen size={14} strokeWidth={2.5} />
                {$strings.landing.mockupLabels.resource}
              </div>
            </div>
            <p class="fm-text">{$strings.landing.samples[3]}</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ TRUST BADGES ============ -->
  <section class="trust-bar">
    <div class="trust-inner">
      {#each $strings.landing.trustBadges as badge}
        <div class="trust-badge">
          <ShieldCheck
            class="trust-icon"
            size={16}
            strokeWidth={2}
            color="var(--color-card-resource)"
          />
          <span>{badge}</span>
        </div>
      {/each}
    </div>
  </section>

  <!-- ============ HOW IT WORKS ============ -->
  <section class="how-section" id="how">
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
                  <div class="sv-blob sv-b1">{$strings.landing.scatterWords[0]}</div>
                  <div class="sv-blob sv-b2">{$strings.landing.scatterWords[1]}</div>
                  <div class="sv-blob sv-b3">{$strings.landing.scatterWords[2]}</div>
                  <div class="sv-arrow">→</div>
                  <div class="sv-card-mini">
                    <div
                      class="sv-card-bar"
                      style="background: var(--color-card-fact)"
                    ></div>
                  </div>
                </div>
              {:else if i === 1}
                <div class="sv-canvas-mini">
                  <div
                    class="sv-dot"
                    style="--x:20%;--y:30%; background: var(--color-card-question)"
                  ></div>
                  <div
                    class="sv-dot"
                    style="--x:60%;--y:20%; background: var(--color-card-fact)"
                  ></div>
                  <div
                    class="sv-dot"
                    style="--x:45%;--y:65%; background: var(--color-card-resource)"
                  ></div>
                  <div
                    class="sv-dot"
                    style="--x:75%;--y:55%; background: var(--color-card-pain)"
                  ></div>
                  <svg
                    class="sv-lines"
                    viewBox="0 0 100 100"
                    preserveAspectRatio="none"
                  >
                    <line
                      x1="22"
                      y1="32"
                      x2="58"
                      y2="22"
                      stroke="var(--color-warm-400)"
                      stroke-width="0.8"
                      opacity="0.6"
                    />
                    <line
                      x1="47"
                      y1="67"
                      x2="22"
                      y2="32"
                      stroke="var(--color-warm-400)"
                      stroke-width="0.8"
                      opacity="0.6"
                    />
                    <line
                      x1="47"
                      y1="67"
                      x2="73"
                      y2="57"
                      stroke="var(--color-warm-400)"
                      stroke-width="0.8"
                      opacity="0.6"
                    />
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
          <CloudFog
            class="ba-svg ba-svg-before"
            size={40}
            color="var(--color-card-pain)"
            strokeWidth={1.5}
          />
        </div>
        <h3 class="ba-title">{$strings.landing.beforeTitle}</h3>
        <ul class="ba-list">
          {#each $strings.landing.beforePoints as point}
            <li class="ba-item ba-item-before">
              <X
                class="ba-x"
                size={14}
                color="var(--color-card-pain)"
                strokeWidth={2.5}
              />
              {point}
            </li>
          {/each}
        </ul>
      </div>
      <div class="ba-arrow">
        <ArrowRight size={48} color="var(--color-warm-400)" strokeWidth={1.5} />
      </div>
      <div class="ba-card ba-after">
        <div class="ba-icon">
          <Sun
            class="ba-svg ba-svg-after"
            size={40}
            color="var(--color-card-resource)"
            strokeWidth={1.5}
          />
        </div>
        <h3 class="ba-title">{$strings.landing.afterTitle}</h3>
        <ul class="ba-list">
          {#each $strings.landing.afterPoints as point}
            <li class="ba-item ba-item-after">
              <Check
                class="ba-check"
                size={14}
                color="var(--color-card-resource)"
                strokeWidth={2.5}
              />
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
                <Sparkles class="lucide-icon" size={28} strokeWidth={1.5} />
              {:else if i === 1}
                <LayoutTemplate
                  class="lucide-icon"
                  size={28}
                  strokeWidth={1.5}
                />
              {:else if i === 2}
                <MapPin class="lucide-icon" size={28} strokeWidth={1.5} />
              {:else}
                <EyeOff class="lucide-icon" size={28} strokeWidth={1.5} />
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
                <ArrowRightCircle
                  class="lucide-icon"
                  size={28}
                  strokeWidth={1.5}
                />
              {:else if i === 1}
                <Target class="lucide-icon" size={28} strokeWidth={1.5} />
              {:else if i === 2}
                <Sparkles class="lucide-icon" size={28} strokeWidth={1.5} />
              {:else if i === 3}
                <Users class="lucide-icon" size={28} strokeWidth={1.5} />
              {:else if i === 4}
                <BookOpen class="lucide-icon" size={28} strokeWidth={1.5} />
              {:else}
                <Hexagon class="lucide-icon" size={28} strokeWidth={1.5} />
              {/if}
            </div>
            <h3 class="persona-title">{persona.title}</h3>
            <p class="persona-desc">{persona.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ SOCIAL PROOF ============ -->
  <section class="social-proof-section">
    <div class="social-proof-inner">
      <div class="section-header">
        <span class="section-kicker">{$strings.landing.socialProofTitle}</span>
        <div class="section-line"></div>
      </div>
      {#if $strings.landing.socialProofItems.length > 0}
        <div class="testimonials-grid">
          {#each $strings.landing.socialProofItems as item}
            <div class="testimonial-card">
              <p class="testimonial-text">"{item.text}"</p>
              <div class="testimonial-author">
                <span class="testimonial-name">{item.name}</span>
                <span class="testimonial-role">{item.role}</span>
              </div>
            </div>
          {/each}
        </div>
      {:else}
        <div class="social-proof-empty">
          <p>{$strings.landing.socialProofEmpty}</p>
        </div>
      {/if}
    </div>
  </section>

  <!-- ============ METHODOLOGY ============ -->
  <section class="methodology-section">
    <div class="methodology-inner">
      <div class="methodology-card">
        <div class="methodology-icon">
          <BrainCircuit
            size={48}
            strokeWidth={1.5}
            color="var(--color-warm-600)"
          />
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

  <!-- ============ PRICING ============ -->
  <section class="pricing-section" id="pricing">
    <div class="pricing-inner">
      <div class="section-header">
        <span class="section-kicker">{$strings.landing.pricing.kicker}</span>
        <div class="section-line"></div>
      </div>

      <div class="pricing-copy">
        <p class="pricing-highlight">{$strings.landing.pricing.highlight}</p>
        <h2 class="pricing-title">{$strings.landing.pricing.title}</h2>
        <p class="pricing-subtitle">{$strings.landing.pricing.subtitle}</p>
      </div>

      <div class="pricing-grid">
        {#each $strings.landing.pricing.plans as plan}
          <article
            class={`pricing-card ${plan.featured ? "pricing-card-featured" : ""}`}
          >
            <div class="pricing-card-head">
              <span
                class={`pricing-badge ${plan.featured ? "pricing-badge-featured" : ""}`}
              >
                {plan.badge}
              </span>
              <h3 class="pricing-plan-name">{plan.name}</h3>
              <div class="pricing-price-row">
                <span class="pricing-price">{plan.price}</span>
                <span class="pricing-period">{plan.period}</span>
              </div>
              <p class="pricing-description">{plan.description}</p>
            </div>

            <ul class="pricing-features">
              {#each plan.features as feature}
                <li class="pricing-feature">
                  <Check
                    class="pricing-check"
                    size={16}
                    color="var(--color-card-resource)"
                    strokeWidth={2.4}
                  />
                  <span>{feature}</span>
                </li>
              {/each}
            </ul>

            <button
              class={`pricing-cta ${plan.featured ? "pricing-cta-featured" : ""}`}
              onclick={handleLogin}
            >
              {plan.cta}
              <ArrowRight size={16} strokeWidth={2.4} />
            </button>
          </article>
        {/each}
      </div>

      <p class="pricing-footer">{$strings.landing.pricing.footer}</p>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section class="faq-section" id="faq">
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
              <ChevronRight
                class={`faq-chevron ${openFaqIndex === i ? "faq-chevron-open" : ""}`}
                size={20}
                strokeWidth={2}
              />
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
    background: var(--color-warm-100);
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
    background: rgba(252, 251, 249, 0.7); /* off-white with alpha */
    backdrop-filter: blur(20px) saturate(1.4);
    border-bottom: 1px solid rgba(28, 25, 23, 0.05); /* near black with low alpha */
  }

  .nav-logo {
    font-family: var(--font-accent);
    font-size: 1.6rem;
    color: var(--color-warm-500);
    letter-spacing: 0.02em;
  }

  .nav-links {
    display: none;
    align-items: center;
    gap: 24px;
  }

  .nav-link {
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 500;
    color: var(--color-warm-600);
    text-decoration: none;
    transition: color 0.2s var(--ease-out);
  }

  .nav-link:hover {
    color: var(--color-warm-800);
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
    background: rgba(28, 25, 23, 0.05);
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
    .nav-cta {
      display: inline-flex;
    }
  }

  @media (min-width: 1024px) {
    .nav-links {
      display: flex;
    }
  }

  /* ============================
     HERO
     ============================ */
  .hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding: 160px 32px 100px;
    overflow: hidden;
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .hero-bg-grid {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.15;
    background-image: linear-gradient(
        to right,
        rgba(28, 25, 23, 0.1) 1px,
        transparent 1px
      ),
      linear-gradient(to bottom, rgba(28, 25, 23, 0.1) 1px, transparent 1px);
    background-size: 40px 40px;
    mask-image: radial-gradient(
      ellipse at center,
      rgba(0, 0, 0, 1) 0%,
      rgba(0, 0, 0, 0) 70%
    );
    -webkit-mask-image: radial-gradient(
      ellipse at center,
      rgba(0, 0, 0, 1) 0%,
      rgba(0, 0, 0, 0) 70%
    );
  }

  .hero-grid-pattern {
    position: absolute;
    inset: 0;
    background-color: transparent;
    background-image: radial-gradient(
      rgba(28, 25, 23, 0.08) 1px,
      transparent 1px
    );
    background-size: 24px 24px;
    mask-image: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 1) 30%,
      rgba(0, 0, 0, 0) 100%
    );
    -webkit-mask-image: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 1) 30%,
      rgba(0, 0, 0, 0) 100%
    );
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
    .hero-inner {
      grid-template-columns: 1fr 1.1fr;
      gap: 64px;
    }
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
    background: rgba(28, 25, 23, 0.04);
    border: 1px solid rgba(28, 25, 23, 0.08);
    border-radius: 100px;
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 500;
    color: var(--color-warm-700);
    letter-spacing: 0.02em;
  }

  .hero-badge-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--color-card-resource);
    box-shadow: 0 0 8px rgba(129, 199, 132, 0.5);
    animation: pulse-dot 2s ease-in-out infinite;
  }

  @keyframes pulse-dot {
    0%,
    100% {
      opacity: 1;
      transform: scale(1);
    }
    50% {
      opacity: 0.6;
      transform: scale(1.3);
    }
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
    color: var(--color-warm-600);
  }

  /* ============================
     HERO CANVAS MOCKUP
     ============================ */
  /* ============================
     HERO FLOATING MOCKUP
     ============================ */
  .floating-mockup {
    position: relative;
    width: 100%;
    max-width: 440px;
    height: 400px;
    margin: 0 auto;
    perspective: 1000px;
  }

  .fm-card {
    position: absolute;
    background: white;
    border-radius: 16px;
    border: 1px solid rgba(28, 25, 23, 0.06);
    padding: 24px;
    font-family: var(--font-body);
    box-shadow:
      0 20px 40px -10px rgba(28, 25, 23, 0.1),
      0 10px 20px -5px rgba(28, 25, 23, 0.05);
    transition:
      transform 0.5s var(--ease-out),
      box-shadow 0.5s var(--ease-out);
  }

  .fm-main {
    width: 320px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotateY(-5deg) rotateX(5deg);
    z-index: 3;
    animation: float-main 6s ease-in-out infinite;
  }

  .fm-sub {
    width: 240px;
    padding: 20px;
  }

  .fm-left {
    top: 15%;
    left: 0;
    transform: translate(-20px, 0) rotate(-6deg) scale(0.9);
    z-index: 2;
    opacity: 0.9;
    animation: float-left 7s ease-in-out infinite alternate;
  }

  .fm-right {
    bottom: 10%;
    right: 0;
    transform: translate(20px, 0) rotate(8deg) scale(0.95);
    z-index: 4;
    animation: float-right 8s ease-in-out infinite alternate;
  }

  .fm-header {
    margin-bottom: 16px;
  }

  .fm-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .fm-title {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 700;
    line-height: 1.3;
    color: var(--color-warm-800);
    margin-bottom: 24px;
  }

  .fm-text {
    font-size: 0.95rem;
    line-height: 1.5;
    color: var(--color-warm-700);
  }

  .fm-footer {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .fm-author {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--color-warm-200);
  }

  @keyframes float-main {
    0%,
    100% {
      transform: translate(-50%, -50%) rotateY(-5deg) rotateX(5deg)
        translateY(0);
    }
    50% {
      transform: translate(-50%, -50%) rotateY(-5deg) rotateX(5deg)
        translateY(-10px);
    }
  }
  @keyframes float-left {
    0% {
      transform: translate(-20px, 0) rotate(-6deg) scale(0.9) translateY(0);
    }
    100% {
      transform: translate(-20px, 0) rotate(-6deg) scale(0.9) translateY(-12px);
    }
  }
  @keyframes float-right {
    0% {
      transform: translate(20px, 0) rotate(8deg) scale(0.95) translateY(0);
    }
    100% {
      transform: translate(20px, 0) rotate(8deg) scale(0.95) translateY(-8px);
    }
  }

  /* ============================
     METRICS BAR
     ============================ */
  .trust-bar {
    background: var(--color-warm-800);
    padding: 24px 32px;
  }

  .trust-inner {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 24px 48px;
  }

  .trust-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 500;
    color: var(--color-warm-200);
    letter-spacing: 0.01em;
  }

  .trust-icon {
    flex-shrink: 0;
  }

  /* ============================
     HOW IT WORKS
     ============================ */
  .how-section {
    position: relative;
    padding: 120px 32px;
    background: linear-gradient(
      180deg,
      var(--color-warm-200) 0%,
      var(--color-warm-100) 100%
    );
  }

  .how-section,
  .pricing-section,
  .faq-section {
    scroll-margin-top: 96px;
  }

  .how-inner {
    max-width: 960px;
    margin: 0 auto;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 56px;
  }

  .section-kicker {
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--color-warm-500);
    white-space: nowrap;
  }

  .section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(
      90deg,
      var(--color-warm-400) 0%,
      transparent 100%
    );
    opacity: 0.3;
  }

  .steps-timeline {
    display: flex;
    flex-direction: column;
  }

  .step {
    display: grid;
    grid-template-columns: 48px 1fr;
    gap: 24px;
    padding: 32px 0;
    border-bottom: 1px solid rgba(28, 25, 23, 0.08);
    position: relative;
  }

  .step:last-child {
    border-bottom: none;
  }

  @media (min-width: 768px) {
    .step {
      grid-template-columns: 48px 1fr 180px;
      align-items: start;
    }
  }

  .step-marker {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .step-num {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: var(--color-warm-800);
    color: #faf3e8;
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 700;
  }

  .step-connector {
    width: 1.5px;
    flex: 1;
    min-height: 40px;
    background: linear-gradient(
      180deg,
      var(--color-warm-800) 0%,
      var(--color-warm-300) 100%
    );
    margin-top: 8px;
  }

  .step-content {
    padding-top: 6px;
  }

  .step-title {
    font-family: var(--font-display);
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 10px;
  }

  .step-desc {
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--color-warm-600);
    max-width: 480px;
  }

  .step-visual {
    display: none;
    align-items: center;
    justify-content: center;
    height: 100px;
  }

  @media (min-width: 768px) {
    .step-visual {
      display: flex;
    }
  }

  .sv-scatter {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .sv-blob {
    padding: 4px 10px;
    background: rgba(28, 25, 23, 0.04);
    border: 1px dashed rgba(28, 25, 23, 0.12);
    border-radius: 8px;
    font-family: var(--font-body);
    font-size: 11px;
    color: var(--color-warm-600);
    animation: wobble 3s ease-in-out infinite alternate;
  }
  .sv-b1 {
    animation-delay: 0s;
  }
  .sv-b2 {
    animation-delay: 0.3s;
  }
  .sv-b3 {
    animation-delay: 0.6s;
  }

  @keyframes wobble {
    0% {
      transform: translateY(0) rotate(0deg);
    }
    100% {
      transform: translateY(-3px) rotate(2deg);
    }
  }

  .sv-arrow {
    font-size: 18px;
    color: var(--color-warm-400);
    margin: 0 4px;
  }

  .sv-card-mini {
    width: 40px;
    height: 48px;
    background: white;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    padding: 6px;
  }
  .sv-card-bar {
    height: 3px;
    border-radius: 3px;
  }

  .sv-canvas-mini {
    position: relative;
    width: 120px;
    height: 80px;
    background: rgba(252, 251, 249, 0.9);
    border: 1px solid rgba(28, 25, 23, 0.1);
    border-radius: 8px;
  }

  .sv-dot {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    top: var(--y);
    left: var(--x);
    transform: translate(-50%, -50%);
  }

  .sv-lines {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }

  .sv-blindspot {
    position: relative;
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .sv-pulse {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px dashed var(--color-warm-400);
    animation: pulse-ring 2.5s ease-in-out infinite;
  }

  @keyframes pulse-ring {
    0%,
    100% {
      transform: scale(1);
      opacity: 0.6;
    }
    50% {
      transform: scale(1.25);
      opacity: 0.2;
    }
  }

  .sv-q {
    font-family: var(--font-display);
    font-size: 24px;
    font-weight: 700;
    color: var(--color-warm-500);
  }

  /* ============================
     BEFORE / AFTER
     ============================ */
  .before-after-section {
    padding: 120px 32px;
    background: var(--color-warm-100);
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

  .ba-x,
  .ba-check {
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
    .ba-arrow {
      transform: rotate(90deg);
    }
  }

  /* ============================
     FEATURES
     ============================ */
  .features-section {
    padding: 120px 32px;
    background: var(--color-warm-200);
  }

  .features-inner {
    max-width: 960px;
    margin: 0 auto;
  }

  .features-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }

  @media (min-width: 768px) {
    .features-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .feature-card {
    padding: 32px 28px;
    background: white;
    border-radius: 20px;
    border: 1px solid rgba(28, 25, 23, 0.05);
    box-shadow: 0 4px 16px -4px rgba(28, 25, 23, 0.04);
    transition:
      transform 0.3s var(--ease-out),
      box-shadow 0.3s var(--ease-out);
  }

  .feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px -8px rgba(28, 25, 23, 0.08);
  }

  .feature-icon {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(28, 25, 23, 0.03);
    border-radius: 14px;
    margin-bottom: 16px;
  }

  .feature-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 8px;
  }

  .feature-desc {
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--color-warm-600);
  }

  /* ============================
     PERSONAS
     ============================ */
  .personas-section {
    padding: 120px 32px;
    background: linear-gradient(
      180deg,
      var(--color-warm-200) 0%,
      var(--color-warm-100) 100%
    );
  }

  .personas-inner {
    max-width: 960px;
    margin: 0 auto;
  }

  .personas-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
  }

  @media (min-width: 640px) {
    .personas-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (min-width: 1024px) {
    .personas-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  .persona-card {
    padding: 28px 24px;
    background: white;
    border-radius: 16px;
    border: 1px solid rgba(28, 25, 23, 0.05);
    text-align: center;
    transition: transform 0.3s var(--ease-out);
  }

  .persona-card:hover {
    transform: translateY(-4px);
  }

  .persona-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(28, 25, 23, 0.03);
    border-radius: 50%;
    margin: 0 auto 14px;
  }

  .persona-title {
    font-family: var(--font-display);
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 8px;
  }

  .persona-desc {
    font-family: var(--font-body);
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--color-warm-600);
  }

  /* ============================
     SOCIAL PROOF
     ============================ */
  .social-proof-section {
    padding: 120px 32px;
    background: var(--color-warm-100);
  }

  .social-proof-inner {
    max-width: 900px;
    margin: 0 auto;
  }

  .testimonials-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }

  @media (min-width: 768px) {
    .testimonials-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .testimonial-card {
    padding: 24px;
    background: white;
    border-radius: 16px;
    border: 1px solid rgba(154, 107, 63, 0.1);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  }

  .testimonial-text {
    font-family: var(--font-body);
    font-size: 15px;
    line-height: 1.6;
    color: var(--color-warm-700);
    font-style: italic;
    margin-bottom: 16px;
  }

  .testimonial-author {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .testimonial-name {
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 600;
    color: var(--color-warm-800);
  }

  .testimonial-role {
    font-family: var(--font-body);
    font-size: 13px;
    color: var(--color-warm-500);
  }

  .social-proof-empty {
    text-align: center;
    padding: 40px 20px;
    border: 2px dashed rgba(154, 107, 63, 0.15);
    border-radius: 16px;
  }

  .social-proof-empty p {
    font-family: var(--font-body);
    font-size: 15px;
    line-height: 1.6;
    color: var(--color-warm-600);
    max-width: 500px;
    margin: 0 auto;
  }

  /* ============================
     METHODOLOGY
     ============================ */
  .methodology-section {
    padding: 120px 32px;
    background: var(--color-warm-200);
  }

  .methodology-inner {
    max-width: 720px;
    margin: 0 auto;
  }

  .methodology-card {
    text-align: center;
    padding: 48px 40px;
    background: white;
    border-radius: 24px;
    border: 1px solid rgba(28, 25, 23, 0.05);
    box-shadow: 0 8px 24px -8px rgba(28, 25, 23, 0.06);
  }

  .methodology-icon {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
  }

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
    padding: 120px 32px;
    background: var(--color-warm-100);
  }

  .result-inner {
    max-width: 800px;
    margin: 0 auto;
  }

  .result-card {
    position: relative;
    padding: 48px 40px;
    background: white;
    border-radius: 24px;
    box-shadow:
      0 32px 64px -16px rgba(28, 25, 23, 0.08),
      0 0 0 1px rgba(28, 25, 23, 0.04);
    overflow: hidden;
  }

  .result-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(
      90deg,
      var(--color-card-question),
      var(--color-card-fact),
      var(--color-card-resource),
      var(--color-card-hypothesis),
      var(--color-card-pain)
    );
  }

  .result-title {
    font-family: var(--font-display);
    font-size: clamp(1.6rem, 3vw, 2.2rem);
    font-weight: 700;
    color: var(--color-warm-800);
    margin-bottom: 16px;
  }

  .result-text {
    font-family: var(--font-body);
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--color-warm-600);
    margin-bottom: 32px;
    max-width: 560px;
  }

  .result-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  .result-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--color-warm-100);
    border-radius: 100px;
    font-family: var(--font-body);
    font-size: 14px;
    color: var(--color-warm-700);
  }

  .pill-check {
    color: var(--color-card-resource);
    font-weight: 700;
    font-size: 13px;
  }

  /* ============================
     PRICING
     ============================ */
  .pricing-section {
    padding: 120px 32px;
    background: linear-gradient(
      180deg,
      var(--color-warm-200) 0%,
      var(--color-warm-100) 100%
    );
  }

  .pricing-inner {
    max-width: 1120px;
    margin: 0 auto;
  }

  .pricing-copy {
    max-width: 760px;
    margin-bottom: 40px;
  }

  .pricing-highlight {
    display: inline-flex;
    align-items: center;
    padding: 8px 14px;
    margin-bottom: 18px;
    border-radius: 999px;
    background: rgba(28, 25, 23, 0.05);
    border: 1px solid rgba(28, 25, 23, 0.08);
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 600;
    color: var(--color-warm-700);
  }

  .pricing-title {
    font-family: var(--font-display);
    font-size: clamp(1.8rem, 3vw, 2.8rem);
    font-weight: 700;
    line-height: 1.12;
    color: var(--color-warm-800);
    margin-bottom: 16px;
    max-width: 16ch;
  }

  .pricing-subtitle {
    max-width: 680px;
    font-family: var(--font-body);
    font-size: 1rem;
    line-height: 1.75;
    color: var(--color-warm-600);
  }

  .pricing-grid {
    display: grid;
    gap: 20px;
  }

  @media (min-width: 960px) {
    .pricing-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
      align-items: stretch;
    }
  }

  .pricing-card {
    display: flex;
    flex-direction: column;
    gap: 28px;
    padding: 30px 28px;
    border-radius: 28px;
    border: 1px solid rgba(28, 25, 23, 0.06);
    background:
      linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(252, 251, 249, 0.9));
    box-shadow:
      0 18px 36px -18px rgba(28, 25, 23, 0.18),
      0 0 0 1px rgba(255, 255, 255, 0.5) inset;
  }

  .pricing-card-featured {
    background:
      radial-gradient(circle at top, rgba(212, 165, 116, 0.18), transparent 42%),
      linear-gradient(180deg, #1f1b18 0%, #141210 100%);
    border-color: rgba(212, 165, 116, 0.26);
    box-shadow:
      0 24px 48px -20px rgba(28, 25, 23, 0.45),
      0 0 0 1px rgba(212, 165, 116, 0.16) inset;
  }

  .pricing-card-head {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .pricing-badge {
    display: inline-flex;
    align-items: center;
    align-self: flex-start;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(28, 25, 23, 0.06);
    border: 1px solid rgba(28, 25, 23, 0.08);
    font-family: var(--font-body);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--color-warm-700);
  }

  .pricing-badge-featured {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.14);
    color: #f5e8d8;
  }

  .pricing-plan-name {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-warm-800);
  }

  .pricing-price-row {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .pricing-price {
    font-family: var(--font-display);
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    line-height: 1;
    color: var(--color-warm-800);
  }

  .pricing-period {
    font-family: var(--font-body);
    font-size: 0.98rem;
    color: var(--color-warm-600);
  }

  .pricing-description {
    font-family: var(--font-body);
    font-size: 0.98rem;
    line-height: 1.7;
    color: var(--color-warm-600);
  }

  .pricing-features {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 20px 0 0;
    border-top: 1px solid rgba(28, 25, 23, 0.08);
  }

  .pricing-feature {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.55;
    color: var(--color-warm-700);
  }

  .pricing-check {
    flex-shrink: 0;
    margin-top: 2px;
  }

  .pricing-cta {
    margin-top: auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    width: 100%;
    padding: 14px 18px;
    border-radius: 14px;
    border: 1px solid rgba(28, 25, 23, 0.1);
    background: rgba(28, 25, 23, 0.03);
    color: var(--color-warm-800);
    font-family: var(--font-body);
    font-size: 15px;
    font-weight: 600;
    transition:
      transform 0.25s var(--ease-out),
      background 0.25s var(--ease-out),
      box-shadow 0.25s var(--ease-out);
  }

  .pricing-cta:hover {
    transform: translateY(-2px);
    background: rgba(28, 25, 23, 0.06);
  }

  .pricing-cta-featured {
    background: #f7efe5;
    color: var(--color-warm-900);
    border-color: rgba(247, 239, 229, 0.25);
    box-shadow: 0 14px 28px -16px rgba(247, 239, 229, 0.5);
  }

  .pricing-cta-featured:hover {
    background: #fff6ea;
  }

  .pricing-footer {
    margin-top: 24px;
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--color-warm-600);
    max-width: 700px;
  }

  .pricing-card-featured .pricing-plan-name,
  .pricing-card-featured .pricing-price,
  .pricing-card-featured .pricing-period,
  .pricing-card-featured .pricing-description,
  .pricing-card-featured .pricing-feature {
    color: #f7efe5;
  }

  .pricing-card-featured .pricing-features {
    border-top-color: rgba(255, 255, 255, 0.12);
  }

  .pricing-card-featured .pricing-check {
    color: #90d992;
  }

  /* ============================
     FAQ
     ============================ */
  .faq-section {
    padding: 120px 32px;
    background: linear-gradient(
      180deg,
      var(--color-warm-100) 0%,
      var(--color-warm-200) 100%
    );
  }

  .faq-inner {
    max-width: 720px;
    margin: 0 auto;
  }

  .faq-list {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .faq-item {
    border-bottom: 1px solid rgba(28, 25, 23, 0.08);
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

  .faq-question:hover {
    color: var(--color-warm-500);
  }

  .faq-chevron {
    color: var(--color-warm-400);
    flex-shrink: 0;
    transition: transform 0.3s var(--ease-spring);
  }

  :global(.faq-chevron-open) {
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
    from {
      opacity: 0;
      transform: translateY(-8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* ============================
     FOOTER CTA
     ============================ */
  .footer-cta {
    position: relative;
    padding: 160px 32px;
    background: var(--color-warm-800);
    overflow: hidden;
  }

  .footer-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }

  .footer-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(60px);
  }
  .footer-orb-1 {
    width: 400px;
    height: 400px;
    top: -30%;
    right: -10%;
    background: radial-gradient(
      circle,
      rgba(154, 107, 63, 0.2) 0%,
      transparent 70%
    );
  }
  .footer-orb-2 {
    width: 300px;
    height: 300px;
    bottom: -20%;
    left: 10%;
    background: radial-gradient(
      circle,
      rgba(149, 117, 205, 0.08) 0%,
      transparent 70%
    );
  }

  .footer-inner {
    position: relative;
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
  }

  .footer-title {
    font-family: var(--font-display);
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 700;
    color: var(--color-warm-100);
    margin-bottom: 32px;
    line-height: 1.15;
  }

  .cta-light {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 16px 32px;
    font-family: var(--font-body);
    font-size: 16px;
    font-weight: 600;
    border: none;
    border-radius: 14px;
    background: #faf3e8;
    color: var(--color-warm-800);
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
    .nav {
      padding: 12px 20px;
    }
    .hero {
      padding: 90px 20px 40px;
    }
    .hero-inner {
      gap: 32px;
    }
    .floating-mockup {
      transform: scale(0.8);
      transform-origin: top center;
      height: 320px;
    }
    .how-section {
      padding: 60px 20px;
    }
    .before-after-section {
      padding: 60px 20px;
    }
    .features-section {
      padding: 60px 20px;
    }
    .personas-section {
      padding: 60px 20px;
    }
    .methodology-section {
      padding: 48px 20px;
    }
    .methodology-card {
      padding: 32px 24px;
    }
    .result-section {
      padding: 60px 20px;
    }
    .result-card {
      padding: 32px 24px;
    }
    .pricing-section {
      padding: 60px 20px;
    }
    .pricing-card {
      padding: 24px 20px;
      border-radius: 22px;
    }
    .faq-section {
      padding: 60px 20px;
    }
    .footer-cta {
      padding: 64px 20px;
    }
    .step {
      grid-template-columns: 40px 1fr;
      gap: 16px;
      padding: 24px 0;
    }
    .step-num {
      width: 34px;
      height: 34px;
      font-size: 14px;
      border-radius: 10px;
    }
  }

  @media (max-width: 420px) {
    .hero-title {
      font-size: 2rem;
    }
    .floating-mockup {
      transform: scale(0.65);
      height: 260px;
    }
  }
</style>
