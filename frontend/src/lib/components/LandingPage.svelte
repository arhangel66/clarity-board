<script lang="ts">
  import { onMount } from "svelte";
  import { trackUpgradeClicked } from "../analytics";
  import { auth } from "../stores/auth";
  import { strings, locale, setLocale, availableLocales } from "../stores/i18n";
  import type { Locale } from "../stores/i18n";
  import {
    ArrowRight,
    Check,
    ChevronRight,
    ShieldCheck,
  } from "lucide-svelte";

  let openFaqIndex = $state(-1);
  let selectedPricingPlanId: string | null = $state(null);
  let navScrolled = $state(false);

  function handleLogin() {
    auth.loginWithGoogle();
  }

  function handlePricingPreview(planId: string) {
    trackUpgradeClicked(planId, "landing_pricing");
    selectedPricingPlanId = planId;
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

    function onScroll() {
      navScrolled = window.scrollY > 20;
    }
    window.addEventListener("scroll", onScroll, { passive: true });

    // Scroll reveal
    let revealObserver: IntersectionObserver | null = null;
    if (typeof IntersectionObserver !== "undefined") {
      revealObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("visible");
              revealObserver?.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15, rootMargin: "0px 0px -40px 0px" },
      );
      document
        .querySelectorAll(".reveal, .reveal-left, .reveal-right, .reveal-scale")
        .forEach((el) => revealObserver?.observe(el));
    }

    return () => {
      root.classList.remove("landing-active");
      document.body.classList.remove("landing-active");
      window.removeEventListener("scroll", onScroll);
      revealObserver?.disconnect();
    };
  });

  const usecaseColors = ["uc-blue", "uc-red", "uc-green", "uc-amber"];
</script>

<div class="landing-root">
  <!-- ============ NAV ============ -->
  <nav class="nav" class:scrolled={navScrolled}>
    <div class="nav-inner">
      <div class="nav-logo">
        <span class="nav-logo-wordmark">{$strings.landing.brand}</span>
      </div>
      <div class="nav-links">
        {#each $strings.landing.navLinks as link}
          <a href="#{link.id}">{link.label}</a>
        {/each}
      </div>
      <div class="nav-right">
        <div class="locale-toggle">
          {#each availableLocales as loc}
            <button
              class="locale-btn"
              class:locale-active={$locale === loc.code}
              onclick={() => handleLocale(loc.code)}
            >
              {loc.label}
            </button>
          {/each}
        </div>
        <button class="nav-cta" onclick={handleLogin}>{$strings.landing.navCta}</button>
      </div>
    </div>
  </nav>

  <!-- ============ HERO ============ -->
  <section class="hero">
    <div class="hero-inner">
      <h1 class="hero-title">{$strings.landing.titleA}<br />{$strings.landing.titleB}</h1>
      <p class="hero-subtitle">{$strings.landing.subtitle}</p>
      <div class="hero-actions">
        <button class="cta-primary" onclick={handleLogin}>
          {$strings.landing.cta}
          <ArrowRight size={18} />
        </button>
        <span class="hero-note">{$strings.landing.note}</span>
      </div>

      <!-- Cork Board Mockup with animated demo -->
      <div class="hero-mockup">
        <div class="mockup-bar">
          <span class="mockup-dot mockup-dot-r"></span>
          <span class="mockup-dot mockup-dot-y"></span>
          <span class="mockup-dot mockup-dot-g"></span>
        </div>
        <div class="mockup-canvas">
          <!-- Voice input bar -->
          <div class="demo-voice-bar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" stroke-width="2" />
              <path
                d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
            <div class="rec-indicator"></div>
            <span class="voice-timer">1:12</span>
            <span class="voice-text-wrap">
              <span class="voice-text-1">{$strings.landing.demoVoice1}</span>
              <span class="voice-text-2">{$strings.landing.demoVoice2}</span>
            </span>
          </div>

          <!-- Root question card -->
          <div class="fc fc-question demo-root-card">
            <div class="fc-emoji">🎯</div>
            <div class="fc-text">{$strings.landing.demoRootQuestion}</div>
            <div class="fc-label">{$strings.card.typeLabels.question}</div>
          </div>

          <!-- Surrounding cards -->
          {#each $strings.landing.demoCards as card, i}
            {@const typeClasses = ["fc-fact", "fc-pain", "fc-resource", "fc-hypothesis", "fc-todo"]}
            {@const maxWidths = ["220px", "220px", "180px", "190px", "160px"]}
            <div
              class="fc {typeClasses[i]} demo-card demo-card-{i + 1}"
              style="max-width:{maxWidths[i]}"
            >
              <div class="fc-emoji">{card.emoji}</div>
              <div class="fc-text">{card.text}</div>
              <div class="fc-label">{card.label}</div>
            </div>
          {/each}

          <!-- Clarity message -->
          <div class="demo-clarity">{$strings.landing.demoClarity}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ TRUST BAR ============ -->
  <div class="trust-bar">
    <div class="trust-inner">
      {#each $strings.landing.trustBadges as badge}
        <div class="trust-badge">
          <ShieldCheck size={16} class="trust-icon" />
          {badge}
        </div>
      {/each}
    </div>
  </div>

  <!-- ============ HOW IT WORKS ============ -->
  <section id="how" class="how-section section-pad">
    <div class="container">
      <div class="section-header reveal">
        <span class="section-kicker">{$strings.landing.howTitle}</span>
        <div class="section-line"></div>
      </div>

      <div class="steps stagger">
        {#each $strings.landing.steps as step, i}
          {@const icons = ["🎙️", "✨", "💡"]}
          <div class="step reveal">
            <div class="step-num">{i + 1}</div>
            <div class="step-icon">{icons[i]}</div>
            <h3>{step.title}</h3>
            <p>{step.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ FEATURES (Zigzag) ============ -->
  <section id="features" class="features-section section-pad">
    <div class="container">
      <div class="section-header reveal">
        <span class="section-kicker">{$strings.landing.featuresTitle}</span>
        <div class="section-line"></div>
      </div>

      <!-- Feature 1: One screen, one problem -->
      <div class="feature-row">
        <div class="feature-text reveal-left">
          <h2>{$strings.landing.featureOneTitle}</h2>
          <p>{$strings.landing.featureOneDesc}</p>
        </div>
        <div class="feature-visual reveal-right">
          <div class="mini-canvas">
            <div class="mc mc-question" style="left:8%;top:12%;transform:rotate(-2deg);width:100px;">
              <span style="font-size:11px;">🎯</span> What matters most?
            </div>
            <div class="mc mc-fact" style="left:40%;top:8%;transform:rotate(1deg);width:110px;">
              <span style="font-size:11px;">📋</span> Job pays well but...
            </div>
            <div class="mc mc-pain" style="left:5%;top:55%;transform:rotate(2deg);width:95px;">
              <span style="font-size:11px;">🔥</span> Fear of change
            </div>
            <div
              class="mc mc-resource"
              style="left:70%;top:15%;transform:rotate(-1deg);width:90px;"
            >
              <span style="font-size:11px;">📚</span> Friend's advice
            </div>
            <div
              class="mc mc-hypothesis"
              style="left:35%;top:50%;transform:rotate(-1.5deg);width:115px;"
            >
              <span style="font-size:11px;">💡</span> Happiness > stability
            </div>
            <div class="mc mc-todo" style="left:65%;top:60%;transform:rotate(1.5deg);width:100px;">
              <span style="font-size:11px;">✅</span> Talk to designers
            </div>
          </div>
        </div>
      </div>

      <!-- Feature 2: Speak, don't type -->
      <div class="feature-row reverse">
        <div class="feature-text reveal-right">
          <h2>{$strings.landing.featureTwoTitle}</h2>
          <p>{$strings.landing.featureTwoDesc}</p>
        </div>
        <div class="feature-visual reveal-left">
          <div class="ai-scene">
            <div class="ai-card">
              <div class="ai-card-emoji">📋</div>
              <div class="ai-card-text">{$strings.landing.demoCards[0]?.text ?? ""}</div>
              <div class="ai-card-label">{$strings.landing.demoCards[0]?.label ?? "fact"}</div>
            </div>
            <div class="ai-input-bar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7a7a7a">
                <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z" stroke-width="2" />
                <path
                  d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
              <span>{$strings.input.voiceHint}</span>
            </div>
            <div class="ai-bubble">
              <div class="ai-bubble-label">AI:</div>
              <div class="ai-bubble-text">{$strings.landing.aiBubble}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Feature 3: AI finds blind spots -->
      <div class="feature-row">
        <div class="feature-text reveal-left">
          <h2>{$strings.landing.featureThreeTitle}</h2>
          <p>{$strings.landing.featureThreeDesc}</p>
        </div>
        <div class="feature-visual reveal-right">
          <div class="blindspot-scene">
            <div class="blindspot-cards">
              <div class="ai-card ai-card-small">
                <div class="ai-card-emoji">📋</div>
                <div class="ai-card-text">{$strings.landing.demoCards[0]?.text ?? ""}</div>
                <div class="ai-card-label">{$strings.landing.demoCards[0]?.label ?? "fact"}</div>
              </div>
              <div class="ai-card ai-card-small ai-card-pain">
                <div class="ai-card-emoji">🔥</div>
                <div class="ai-card-text">{$strings.landing.demoCards[1]?.text ?? ""}</div>
                <div class="ai-card-label">{$strings.landing.demoCards[1]?.label ?? "pain"}</div>
              </div>
            </div>
            <div class="ai-bubble">
              <div class="ai-bubble-label">AI:</div>
              <div class="ai-bubble-text">
                {$locale === "ru"
                  ? "Вы говорите о страхе, но чего именно боитесь? Потери дохода, идентичности, или чего-то другого?"
                  : "You mention fear, but what specifically are you afraid of losing? Is it income, identity, or something else?"}
              </div>
            </div>
            <div class="insight-card">
              <div class="insight-emoji">🎯</div>
              <div class="insight-text">
                {$locale === "ru"
                  ? "Дело не в деньгах — это страх публичного провала"
                  : "It's not the money — it's the fear of failing publicly"}
              </div>
              <div class="insight-label">
                {$locale === "ru" ? "новый инсайт" : "new insight"}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ USE CASES ============ -->
  <section class="usecases-section section-pad">
    <div class="container">
      <div class="section-header reveal">
        <span class="section-kicker">{$strings.landing.useCasesTitle}</span>
        <div class="section-line"></div>
      </div>

      <div class="usecases-grid stagger">
        {#each $strings.landing.useCases as useCase, i}
          <div class="usecase-card {usecaseColors[i]} reveal">
            <div class="usecase-icon">{useCase.emoji}</div>
            <h3>{useCase.title}</h3>
            <p>{useCase.desc}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ PRICING ============ -->
  <section id="pricing" class="pricing-section section-pad">
    <div class="container">
      <div class="section-header reveal">
        <span class="section-kicker">{$strings.landing.pricing.kicker}</span>
        <div class="section-line"></div>
        <h2 class="section-title">{$strings.landing.pricing.title}</h2>
      </div>
      <p class="pricing-highlight">{$strings.landing.pricing.highlight}</p>

      <div class="pricing-grid stagger">
        {#each $strings.landing.pricing.plans as plan}
          <article class="pricing-card reveal" class:pricing-featured={plan.featured}>
            {#if plan.featured}
              <div class="pricing-featured-badge">{plan.badge}</div>
              <div class="pricing-badge" style="visibility:hidden;">.</div>
            {:else}
              <div class="pricing-badge">{plan.badge}</div>
            {/if}
            <div class="pricing-name">{plan.name}</div>
            <div class="pricing-price-row">
              <span class="pricing-price">{plan.price}</span>
              <span class="pricing-period">{plan.period}</span>
            </div>
            <p class="pricing-desc">{plan.description}</p>
            <ul class="pricing-features">
              {#each plan.features as feature}
                <li>
                  <Check size={16} class="pricing-check" />
                  {feature}
                </li>
              {/each}
            </ul>
            <button
              class="pricing-cta"
              class:pricing-cta-featured={plan.featured}
              class:pricing-cta-default={!plan.featured}
              onclick={() => handlePricingPreview(plan.id)}
            >
              {plan.landingCta}
            </button>
          </article>
        {/each}
      </div>

      {#if selectedPricingPlanId}
        <div class="pricing-preview">
          <p class="pricing-preview-text">
            {$strings.access.paywallPreview.replace(
              "{plan}",
              $strings.landing.pricing.plans.find((p) => p.id === selectedPricingPlanId)?.name ??
                "",
            )}
          </p>
          <p class="pricing-preview-note">{$strings.access.paywallNote}</p>
          <button class="cta-primary pricing-preview-cta" onclick={handleLogin}>
            {$strings.landing.pricing.previewAction}
          </button>
        </div>
      {/if}

      <p class="pricing-footer-text">{$strings.landing.pricing.footer}</p>
    </div>
  </section>

  <!-- ============ FAQ ============ -->
  <section id="faq" class="faq-section section-pad">
    <div class="container">
      <div class="section-header reveal">
        <span class="section-kicker">{$strings.landing.faqTitle}</span>
        <div class="section-line"></div>
      </div>

      <div class="faq-list reveal">
        {#each $strings.landing.faq as item, i}
          <div class="faq-item">
            <button class="faq-question" onclick={() => toggleFaq(i)}>
              <span>{item.q}</span>
              <ChevronRight size={20} class="faq-chevron {openFaqIndex === i ? 'open' : ''}" />
            </button>
            <div class="faq-answer" class:open={openFaqIndex === i}>
              <p>{item.a}</p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- ============ FINAL CTA ============ -->
  <section class="final-cta">
    <h2 class="reveal">{$strings.landing.ctaRepeat}</h2>
    <p>{$strings.landing.note}</p>
    <button class="cta-primary" onclick={handleLogin}>
      {$strings.landing.cta}
      <ArrowRight size={18} />
    </button>
  </section>

  <!-- ============ FOOTER ============ -->
  <footer class="footer">
    <div class="footer-inner">
      <span class="footer-logo">{$strings.landing.brand}</span>
      <span class="footer-copy">&copy; 2025 {$strings.landing.brand}</span>
    </div>
  </footer>
</div>

<style>
  /* ===== LANDING GLOBAL OVERRIDES ===== */
  :global(html.landing-active),
  :global(body.landing-active) {
    overflow: auto !important;
    height: auto !important;
    font-family: "DM Sans", system-ui, sans-serif !important;
    background: #fff !important;
  }
  :global(body.landing-active) {
    display: block !important;
  }
  :global(body.landing-active #app) {
    display: block !important;
    height: auto !important;
  }

  /* ===== RESET & PALETTE ===== */
  :root {
    --brand: #4b89c7;
    --brand-dark: #3a6fa3;
    --warm-100: #fcfbf9;
    --warm-200: #f4f3ec;
    --warm-300: #e4e2da;
    --warm-400: #d0cec5;
    --warm-700: #4a453f;
    --warm-800: #1c1917;
    --fact: #5b9bd5;
    --fact-light: #e8f1f8;
    --pain: #e57373;
    --pain-light: #fce8e8;
    --resource: #81c784;
    --resource-light: #e8f5e9;
    --hypothesis: #ffb74d;
    --hypothesis-light: #fff8e1;
    --question: #9575cd;
    --question-light: #ede7f6;
    --todo: #14b8a6;
    --todo-light: #e6f8f5;
    --shadow-card: 0 3px 10px rgba(0, 0, 0, 0.12), 0 1px 3px rgba(0, 0, 0, 0.08);
    --shadow-pin: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .landing-root {
    font-family: "DM Sans", system-ui, sans-serif;
    color: var(--warm-800);
    line-height: 1.6;
    background: #fff;
    width: 100%;
    min-height: 100vh;
  }

  /* ===== LAYOUT ===== */
  .container {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 24px;
  }
  .section-pad {
    padding: 96px 0;
  }

  /* ===== NAV ===== */
  .nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--warm-300);
    transition: box-shadow 0.3s, background 0.3s;
  }
  .nav.scrolled {
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
    background: rgba(255, 255, 255, 0.97);
  }
  .nav-inner {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 24px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .nav-logo {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 22px;
    color: var(--warm-800);
  }
  .nav-links {
    display: flex;
    gap: 32px;
  }
  .nav-links a {
    font-size: 14px;
    font-weight: 500;
    color: var(--warm-700);
    text-decoration: none;
    transition: color 0.15s;
  }
  .nav-links a:hover {
    color: var(--warm-800);
  }
  .nav-right {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .locale-toggle {
    display: flex;
    gap: 4px;
    background: var(--warm-200);
    border-radius: 8px;
    padding: 2px;
  }
  .locale-btn {
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    color: var(--warm-700);
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.15s;
  }
  .locale-active {
    background: #fff;
    color: var(--warm-800);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  .nav-cta {
    background: var(--warm-800);
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    padding: 10px 24px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background 0.15s;
  }
  .nav-cta:hover {
    background: #2a2520;
  }

  /* ===== HERO ===== */
  .hero {
    padding: 48px 0 64px;
    background: linear-gradient(180deg, var(--warm-100) 0%, #fff 100%);
    position: relative;
    overflow: hidden;
  }
  .hero-inner {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 24px;
    text-align: center;
  }
  .hero-title {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: clamp(30px, 4vw, 46px);
    line-height: 1.2;
    color: var(--warm-800);
    max-width: 680px;
    margin: 0 auto 20px;
    opacity: 0;
    transform: translateY(24px);
    animation: heroEntrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.25s forwards;
  }
  .hero-subtitle {
    font-size: 18px;
    line-height: 1.7;
    color: var(--warm-700);
    max-width: 600px;
    margin: 0 auto 36px;
    opacity: 0;
    transform: translateY(24px);
    animation: heroEntrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;
  }
  .hero-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    opacity: 0;
    transform: translateY(24px);
    animation: heroEntrance 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.55s forwards;
  }
  .hero-note {
    font-size: 13px;
    color: var(--warm-700);
    opacity: 0.7;
  }

  /* ===== CTA BUTTON ===== */
  .cta-primary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--warm-800);
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    padding: 14px 32px;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(28, 25, 23, 0.15);
    position: relative;
    overflow: hidden;
  }
  .cta-primary:hover {
    background: #2a2520;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(28, 25, 23, 0.2);
  }
  .cta-primary::after {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
    animation: shimmer 3s ease-in-out infinite;
  }

  /* ===== HERO MOCKUP — Cork Board ===== */
  .hero-mockup {
    margin: 56px auto 0;
    max-width: 880px;
    border-radius: 16px;
    overflow: hidden;
    box-shadow:
      0 32px 64px -12px rgba(0, 0, 0, 0.18),
      0 0 0 1px rgba(0, 0, 0, 0.04);
    opacity: 0;
    transform: translateY(40px) scale(0.97);
    animation: heroMockup 1s cubic-bezier(0.16, 1, 0.3, 1) 0.7s forwards;
  }
  .mockup-bar {
    background: #2a2520;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .mockup-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .mockup-dot-r {
    background: #ff5f57;
  }
  .mockup-dot-y {
    background: #ffbd2e;
  }
  .mockup-dot-g {
    background: #27c93f;
  }
  .mockup-canvas {
    position: relative;
    height: 400px;
    overflow: hidden;
    background:
      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.08'/%3E%3C/svg%3E"),
      radial-gradient(ellipse at 30% 20%, #e6c9a8 0%, #d4a574 50%, #c49660 100%);
    background-blend-mode: soft-light, normal;
  }

  /* ===== REALISTIC CARD ===== */
  .fc {
    position: absolute;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.88));
    border-radius: 4px;
    padding: 14px 16px;
    box-shadow:
      var(--shadow-card),
      inset 0 0 30px rgba(0, 0, 0, 0.02);
    min-width: 150px;
    max-width: 220px;
    font-family: Georgia, "Times New Roman", serif;
    color: #3d3d3d;
  }
  .fc::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    border-radius: 4px 4px 0 0;
  }
  .fc::before {
    content: "";
    position: absolute;
    top: -7px;
    left: 50%;
    transform: translateX(-50%);
    width: 16px;
    height: 16px;
    border-radius: 50%;
    box-shadow: var(--shadow-pin);
    z-index: 2;
  }
  .fc-fact::after {
    background: var(--fact);
  }
  .fc-fact::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .fc-pain::after {
    background: var(--pain);
  }
  .fc-pain::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .fc-resource::after {
    background: var(--resource);
  }
  .fc-resource::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .fc-hypothesis::after {
    background: var(--hypothesis);
  }
  .fc-hypothesis::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .fc-question::after {
    background: var(--question);
  }
  .fc-question::before {
    background: radial-gradient(circle at 30% 30%, #b39ddb, #7e57c2);
    width: 20px;
    height: 20px;
    top: -8px;
  }
  .fc-todo::after {
    background: var(--todo);
  }
  .fc-todo::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .fc-emoji {
    font-size: 1.6em;
    margin-bottom: 6px;
    filter: drop-shadow(1px 1px 1px rgba(0, 0, 0, 0.1));
  }
  .fc-text {
    font-size: 13px;
    line-height: 1.45;
  }
  .fc-label {
    font-family: "Caveat", cursive;
    font-size: 12px;
    color: #7a7a7a;
    text-align: right;
    margin-top: 6px;
  }

  /* ===== DEMO FLOW ANIMATION (30s cycle) ===== */
  .demo-voice-bar {
    position: absolute;
    bottom: 16px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 255, 255, 0.95);
    border-radius: 24px;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    font-size: 14px;
    color: #3d3d3d;
    z-index: 10;
    white-space: nowrap;
    opacity: 0;
    animation: voice-bar-flow 30s ease-in-out infinite;
  }
  .demo-voice-bar svg {
    opacity: 0.5;
    flex-shrink: 0;
  }
  .rec-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #e53935;
    flex-shrink: 0;
    animation: rec-blink 1s ease-in-out infinite;
  }
  .voice-timer {
    font-size: 12px;
    font-weight: 600;
    color: #e53935;
    font-variant-numeric: tabular-nums;
    opacity: 0;
    flex-shrink: 0;
    animation: timer-flow 30s linear infinite;
  }
  .voice-text-wrap {
    position: relative;
    overflow: hidden;
    white-space: nowrap;
  }
  .voice-text-1,
  .voice-text-2 {
    display: inline-block;
    max-width: 0;
    overflow: hidden;
    white-space: nowrap;
    vertical-align: bottom;
  }
  .voice-text-1 {
    animation: vt1 30s linear infinite;
  }
  .voice-text-2 {
    position: absolute;
    left: 0;
    top: 0;
    animation: vt2 30s linear infinite;
  }

  /* Root question card */
  .demo-root-card {
    position: absolute;
    top: 42%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0;
    z-index: 5;
    min-width: 220px;
    max-width: 260px;
    padding: 20px 24px;
    text-align: center;
    animation: root-card-flow 30s ease-out infinite;
  }
  .demo-root-card::before {
    background: radial-gradient(circle at 30% 30%, #b39ddb, #7e57c2) !important;
    width: 20px !important;
    height: 20px !important;
    top: -8px !important;
  }
  .demo-root-card .fc-emoji {
    font-size: 2em;
  }
  .demo-root-card .fc-text {
    font-size: 15px;
    line-height: 1.45;
  }

  /* Surrounding cards positions & animations */
  .demo-card {
    position: absolute;
    opacity: 0;
    z-index: 3;
  }
  .demo-card-1 {
    top: 14%;
    left: 12%;
    animation: card1-pop 30s ease-out infinite;
  }
  .demo-card-2 {
    top: 10%;
    right: 12%;
    left: auto;
    animation: card2-pop 30s ease-out infinite;
  }
  .demo-card-3 {
    top: 58%;
    left: 8%;
    animation: card3-pop 30s ease-out infinite;
  }
  .demo-card-4 {
    top: 54%;
    right: 8%;
    left: auto;
    animation: card4-pop 30s ease-out infinite;
  }
  .demo-card-5 {
    top: 32%;
    right: 4%;
    left: auto;
    animation: card5-pop 30s ease-out infinite;
  }

  /* Clarity message */
  .demo-clarity {
    position: absolute;
    bottom: 56px;
    left: 50%;
    transform: translateX(-50%);
    font-family: "Caveat", cursive;
    font-size: 22px;
    color: var(--warm-800);
    letter-spacing: 0.02em;
    opacity: 0;
    z-index: 10;
    white-space: nowrap;
    text-shadow: 0 1px 4px rgba(255, 255, 255, 0.8);
    animation: clarity-flow 30s ease-in-out infinite;
  }

  /* ===== TRUST BAR ===== */
  .trust-bar {
    padding: 24px 0;
    border-bottom: 1px solid var(--warm-300);
    background: var(--warm-100);
  }
  .trust-inner {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
  }
  .trust-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 500;
    color: var(--warm-700);
  }
  .trust-badge :global(svg) {
    color: var(--resource);
  }

  /* ===== SECTION HEADER ===== */
  .section-header {
    text-align: center;
    margin-bottom: 56px;
  }
  .section-kicker {
    font-family: "DM Sans", sans-serif;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--warm-700);
  }
  .section-line {
    width: 40px;
    height: 2px;
    background: var(--warm-300);
    margin: 12px auto 0;
  }
  .section-title {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: clamp(28px, 3.5vw, 40px);
    line-height: 1.2;
    color: var(--warm-800);
    margin-top: 16px;
  }

  /* ===== HOW IT WORKS ===== */
  .how-section {
    background: #fff;
  }
  .steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 48px;
    max-width: 900px;
    margin: 0 auto;
    position: relative;
  }
  .steps::before,
  .steps::after {
    content: "";
    position: absolute;
    top: 32px;
    width: calc(33.3% - 48px);
    height: 2px;
    background: repeating-linear-gradient(
      90deg,
      var(--warm-300) 0,
      var(--warm-300) 6px,
      transparent 6px,
      transparent 12px
    );
  }
  .steps::before {
    left: calc(16.6% + 32px);
  }
  .steps::after {
    left: calc(50% + 16px);
  }
  .step {
    text-align: center;
  }
  .step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 20px;
    color: var(--brand);
    background: rgba(75, 137, 199, 0.08);
    border: 2px solid rgba(75, 137, 199, 0.15);
    margin-bottom: 20px;
  }
  .step-icon {
    font-size: 36px;
    margin-bottom: 8px;
  }
  .step h3 {
    font-family: "DM Sans", sans-serif;
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 8px;
    color: var(--warm-800);
  }
  .step p {
    font-size: 14px;
    line-height: 1.6;
    color: var(--warm-700);
  }

  /* ===== FEATURES (Zigzag) ===== */
  .features-section {
    background: var(--warm-100);
  }
  .feature-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    align-items: center;
    max-width: 1000px;
    margin: 0 auto;
  }
  .feature-row + .feature-row {
    margin-top: 96px;
  }
  .feature-row.reverse .feature-text {
    order: 2;
  }
  .feature-row.reverse .feature-visual {
    order: 1;
  }
  .feature-text h2 {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: clamp(26px, 3vw, 36px);
    line-height: 1.2;
    color: var(--warm-800);
    margin-bottom: 16px;
  }
  .feature-text p {
    font-size: 16px;
    line-height: 1.7;
    color: var(--warm-700);
  }
  .feature-visual {
    background: var(--warm-200);
    border-radius: 16px;
    padding: 32px;
    min-height: 300px;
    position: relative;
    overflow: hidden;
  }

  /* Mini canvas scene */
  .mini-canvas {
    position: relative;
    width: 100%;
    height: 240px;
    background: radial-gradient(ellipse at 30% 20%, #e6c9a8 0%, #d4a574 50%, #c49660 100%);
    border-radius: 8px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  .mc {
    position: absolute;
    background: rgba(255, 255, 255, 0.92);
    border-radius: 3px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
    padding: 6px 8px;
    font-family: Georgia, serif;
    font-size: 10px;
    color: #3d3d3d;
    line-height: 1.3;
  }
  .mc::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    border-radius: 3px 3px 0 0;
  }
  .mc::before {
    content: "";
    position: absolute;
    top: -4px;
    left: 50%;
    transform: translateX(-50%);
    width: 10px;
    height: 10px;
    border-radius: 50%;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }
  .mc-fact::after {
    background: var(--fact);
  }
  .mc-fact::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .mc-pain::after {
    background: var(--pain);
  }
  .mc-pain::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .mc-resource::after {
    background: var(--resource);
  }
  .mc-resource::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .mc-hypothesis::after {
    background: var(--hypothesis);
  }
  .mc-hypothesis::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }
  .mc-question::after {
    background: var(--question);
  }
  .mc-question::before {
    background: radial-gradient(circle at 30% 30%, #b39ddb, #7e57c2);
    width: 12px;
    height: 12px;
    top: -5px;
  }
  .mc-todo::after {
    background: var(--todo);
  }
  .mc-todo::before {
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
  }

  /* AI input scene */
  .ai-scene {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .ai-card {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 4px;
    padding: 14px 16px;
    box-shadow: var(--shadow-card);
    position: relative;
    max-width: 260px;
  }
  .ai-card::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    border-radius: 4px 4px 0 0;
    background: var(--fact);
  }
  .ai-card::before {
    content: "";
    position: absolute;
    top: -7px;
    left: 50%;
    transform: translateX(-50%);
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #ff6b6b, #c0392b);
    box-shadow: var(--shadow-pin);
    z-index: 2;
  }
  .ai-card-pain::after {
    background: var(--pain);
  }
  .ai-card-emoji {
    font-size: 1.4em;
    margin-bottom: 4px;
  }
  .ai-card-text {
    font-family: Georgia, serif;
    font-size: 14px;
    color: #3d3d3d;
    line-height: 1.4;
  }
  .ai-card-label {
    font-family: "Caveat", cursive;
    font-size: 12px;
    color: #7a7a7a;
    text-align: right;
    margin-top: 4px;
  }
  .ai-card-small {
    max-width: 180px;
  }
  .ai-card-small .ai-card-text {
    font-size: 13px;
  }
  .ai-input-bar {
    background: #fff;
    border-radius: 24px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    border: 1px solid var(--warm-300);
  }
  .ai-input-bar span {
    font-size: 14px;
    color: #7a7a7a;
  }

  /* AI bubble */
  .ai-bubble {
    background: rgba(75, 137, 199, 0.06);
    border-radius: 12px;
    padding: 12px 16px;
    border-left: 3px solid var(--brand);
    max-width: 340px;
  }
  .ai-bubble-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--brand);
    margin-bottom: 4px;
  }
  .ai-bubble-text {
    font-size: 14px;
    color: var(--warm-700);
    line-height: 1.5;
  }

  /* Blindspot scene */
  .blindspot-scene {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .blindspot-cards {
    display: flex;
    gap: 12px;
  }
  .insight-card {
    position: relative;
    max-width: 220px;
    background: rgba(255, 255, 255, 0.92);
    border-radius: 4px;
    padding: 14px 16px;
    box-shadow: var(--shadow-card);
    border-left: 3px solid var(--question);
    opacity: 0.95;
  }
  .insight-emoji {
    font-size: 1.2em;
    margin-bottom: 4px;
  }
  .insight-text {
    font-family: Georgia, serif;
    font-size: 13px;
    color: #3d3d3d;
    line-height: 1.4;
  }
  .insight-label {
    font-family: "Caveat", cursive;
    font-size: 12px;
    color: #7a7a7a;
    text-align: right;
    margin-top: 4px;
  }

  /* ===== USE CASES ===== */
  .usecases-section {
    background: #fff;
  }
  .usecases-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    max-width: 800px;
    margin: 0 auto;
  }
  .usecase-card {
    background: #fff;
    border-radius: 16px;
    padding: 32px;
    border: 2px solid transparent;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition:
      transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
      box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .usecase-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  }
  .uc-blue {
    border-color: rgba(91, 155, 213, 0.3);
  }
  .uc-red {
    border-color: rgba(229, 115, 115, 0.3);
  }
  .uc-green {
    border-color: rgba(129, 199, 132, 0.3);
  }
  .uc-amber {
    border-color: rgba(255, 183, 77, 0.3);
  }
  .usecase-icon {
    font-size: 32px;
    margin-bottom: 16px;
  }
  .usecase-card h3 {
    font-family: "DM Sans", sans-serif;
    font-weight: 700;
    font-size: 18px;
    color: var(--warm-800);
    margin-bottom: 8px;
  }
  .usecase-card p {
    font-size: 14px;
    line-height: 1.6;
    color: var(--warm-700);
  }

  /* ===== PRICING ===== */
  .pricing-section {
    background: var(--warm-100);
  }
  .pricing-highlight {
    text-align: center;
    font-size: 15px;
    color: var(--warm-700);
    margin: -32px auto 48px;
    max-width: 600px;
  }
  .pricing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    max-width: 900px;
    margin: 0 auto;
  }
  .pricing-card {
    background: #fff;
    border-radius: 16px;
    padding: 32px;
    border: 1px solid var(--warm-300);
    display: flex;
    flex-direction: column;
    transition:
      transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
      box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .pricing-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  }
  .pricing-featured {
    border: 2px solid var(--warm-800);
    position: relative;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  }
  .pricing-featured-badge {
    position: absolute;
    top: -13px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--warm-800);
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 16px;
    border-radius: 100px;
    white-space: nowrap;
  }
  .pricing-badge {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--warm-700);
    margin-bottom: 8px;
  }
  .pricing-name {
    font-weight: 700;
    font-size: 20px;
    color: var(--warm-800);
    margin-bottom: 4px;
  }
  .pricing-price-row {
    display: flex;
    align-items: baseline;
    gap: 4px;
  }
  .pricing-price {
    font-family: "Fraunces", serif;
    font-weight: 800;
    font-size: 42px;
    color: var(--warm-800);
    line-height: 1;
  }
  .pricing-period {
    font-size: 14px;
    color: var(--warm-700);
  }
  .pricing-desc {
    font-size: 13px;
    color: var(--warm-700);
    margin: 12px 0 20px;
    line-height: 1.5;
  }
  .pricing-features {
    list-style: none;
    flex: 1;
    margin-bottom: 24px;
    padding: 0;
  }
  .pricing-features li {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 14px;
    color: var(--warm-700);
    padding: 6px 0;
  }
  .pricing-features :global(.pricing-check) {
    color: var(--resource);
    flex-shrink: 0;
    margin-top: 2px;
  }
  .pricing-cta {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    text-align: center;
    border: none;
    cursor: pointer;
    transition: all 0.15s;
  }
  .pricing-cta-default {
    background: var(--warm-200);
    color: var(--warm-800);
  }
  .pricing-cta-default:hover {
    background: var(--warm-300);
  }
  .pricing-cta-featured {
    background: var(--warm-800);
    color: #fff;
  }
  .pricing-cta-featured:hover {
    background: #2a2520;
  }
  .pricing-preview {
    text-align: center;
    margin-top: 32px;
    padding: 24px;
    background: #fff;
    border-radius: 12px;
    border: 1px solid var(--warm-300);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  .pricing-preview-text {
    font-size: 16px;
    font-weight: 600;
    color: var(--warm-800);
    margin-bottom: 8px;
  }
  .pricing-preview-note {
    font-size: 14px;
    color: var(--warm-700);
    margin-bottom: 16px;
  }
  .pricing-preview-cta {
    font-size: 14px;
    padding: 10px 24px;
  }
  .pricing-footer-text {
    text-align: center;
    margin-top: 32px;
    font-size: 13px;
    color: var(--warm-700);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  /* ===== FAQ ===== */
  .faq-section {
    background: #fff;
  }
  .faq-list {
    max-width: 680px;
    margin: 0 auto;
  }
  .faq-item {
    border-bottom: 1px solid var(--warm-300);
  }
  .faq-question {
    width: 100%;
    padding: 20px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 16px;
    font-weight: 600;
    color: var(--warm-800);
    text-align: left;
    background: none;
    border: none;
    cursor: pointer;
  }
  .faq-question :global(.faq-chevron) {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    transition: transform 0.2s;
    color: var(--warm-400);
  }
  .faq-question :global(.faq-chevron.open) {
    transform: rotate(90deg);
  }
  .faq-answer {
    overflow: hidden;
    max-height: 0;
    opacity: 0;
    transition:
      max-height 0.4s cubic-bezier(0.16, 1, 0.3, 1),
      opacity 0.3s ease,
      padding 0.3s ease;
    padding: 0;
  }
  .faq-answer.open {
    max-height: 200px;
    opacity: 0.8;
    padding: 0 0 20px;
  }
  .faq-answer p {
    font-size: 15px;
    line-height: 1.7;
    color: var(--warm-700);
  }

  /* ===== FINAL CTA ===== */
  .final-cta {
    padding: 80px 0;
    text-align: center;
    background: linear-gradient(180deg, var(--warm-100), #fff);
  }
  .final-cta h2 {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: clamp(28px, 3.5vw, 40px);
    color: var(--warm-800);
    margin-bottom: 12px;
  }
  .final-cta p {
    font-size: 16px;
    color: var(--warm-700);
    margin-bottom: 32px;
  }

  /* ===== FOOTER ===== */
  .footer {
    padding: 24px 0;
    border-top: 1px solid var(--warm-300);
  }
  .footer-inner {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 13px;
    color: var(--warm-400);
  }
  .footer-logo {
    font-family: "Fraunces", serif;
    font-weight: 700;
    font-size: 16px;
    color: var(--warm-700);
  }

  /* ===== SCROLL REVEAL ===== */
  :global(.reveal) {
    opacity: 0;
    transform: translateY(32px);
    transition:
      opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
      transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
  }
  :global(.reveal.visible) {
    opacity: 1;
    transform: translateY(0);
  }
  :global(.reveal-left) {
    opacity: 0;
    transform: translateX(-40px);
    transition:
      opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
      transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
  }
  :global(.reveal-left.visible) {
    opacity: 1;
    transform: translateX(0);
  }
  :global(.reveal-right) {
    opacity: 0;
    transform: translateX(40px);
    transition:
      opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1),
      transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
  }
  :global(.reveal-right.visible) {
    opacity: 1;
    transform: translateX(0);
  }

  /* Stagger delays */
  .stagger > :nth-child(1) {
    transition-delay: 0ms;
  }
  .stagger > :nth-child(2) {
    transition-delay: 100ms;
  }
  .stagger > :nth-child(3) {
    transition-delay: 200ms;
  }
  .stagger > :nth-child(4) {
    transition-delay: 300ms;
  }

  /* ===== KEYFRAMES ===== */
  @keyframes heroEntrance {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  @keyframes heroMockup {
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
  @keyframes shimmer {
    0%,
    100% {
      left: -100%;
    }
    50% {
      left: 100%;
    }
  }
  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.4;
    }
  }
  @keyframes rec-blink {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.3;
    }
  }
  @keyframes voice-bar-flow {
    0% {
      opacity: 0;
      transform: translateX(-50%) translateY(8px);
    }
    3.3% {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    30% {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    33.3% {
      opacity: 0;
      transform: translateX(-50%) translateY(0);
    }
    100% {
      opacity: 0;
    }
  }
  @keyframes timer-flow {
    0%,
    19% {
      opacity: 0;
    }
    21% {
      opacity: 1;
    }
    30% {
      opacity: 1;
    }
    33.3% {
      opacity: 0;
    }
    100% {
      opacity: 0;
    }
  }
  @keyframes vt1 {
    0%,
    3.3% {
      max-width: 0;
      opacity: 1;
    }
    10% {
      max-width: 400px;
      opacity: 1;
    }
    18% {
      max-width: 400px;
      opacity: 1;
    }
    20% {
      max-width: 400px;
      opacity: 0;
    }
    100% {
      max-width: 400px;
      opacity: 0;
    }
  }
  @keyframes vt2 {
    0%,
    19% {
      max-width: 0;
      opacity: 0;
    }
    20% {
      max-width: 0;
      opacity: 1;
    }
    30% {
      max-width: 500px;
      opacity: 1;
    }
    33.3% {
      max-width: 500px;
      opacity: 0;
    }
    100% {
      max-width: 500px;
      opacity: 0;
    }
  }
  @keyframes root-card-flow {
    0%,
    13.3% {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.8);
    }
    16.7% {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
    93.3% {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
    100% {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.95);
    }
  }
  @keyframes card1-pop {
    0%,
    32% {
      opacity: 0;
      transform: translateY(16px) rotate(-2deg) scale(0.85);
    }
    35% {
      opacity: 1;
      transform: translateY(0) rotate(-2deg) scale(1);
    }
    93.3% {
      opacity: 1;
      transform: translateY(0) rotate(-2deg) scale(1);
    }
    100% {
      opacity: 0;
      transform: translateY(0) rotate(-2deg) scale(0.95);
    }
  }
  @keyframes card2-pop {
    0%,
    34% {
      opacity: 0;
      transform: translateY(16px) rotate(1.5deg) scale(0.85);
    }
    37% {
      opacity: 1;
      transform: translateY(0) rotate(1.5deg) scale(1);
    }
    93.3% {
      opacity: 1;
      transform: translateY(0) rotate(1.5deg) scale(1);
    }
    100% {
      opacity: 0;
      transform: translateY(0) rotate(1.5deg) scale(0.95);
    }
  }
  @keyframes card3-pop {
    0%,
    39% {
      opacity: 0;
      transform: translateY(16px) rotate(2deg) scale(0.85);
    }
    42% {
      opacity: 1;
      transform: translateY(0) rotate(2deg) scale(1);
    }
    93.3% {
      opacity: 1;
      transform: translateY(0) rotate(2deg) scale(1);
    }
    100% {
      opacity: 0;
      transform: translateY(0) rotate(2deg) scale(0.95);
    }
  }
  @keyframes card4-pop {
    0%,
    41% {
      opacity: 0;
      transform: translateY(16px) rotate(-1.5deg) scale(0.85);
    }
    44% {
      opacity: 1;
      transform: translateY(0) rotate(-1.5deg) scale(1);
    }
    93.3% {
      opacity: 1;
      transform: translateY(0) rotate(-1.5deg) scale(1);
    }
    100% {
      opacity: 0;
      transform: translateY(0) rotate(-1.5deg) scale(0.95);
    }
  }
  @keyframes card5-pop {
    0%,
    46% {
      opacity: 0;
      transform: translateY(16px) rotate(1deg) scale(0.85);
    }
    49% {
      opacity: 1;
      transform: translateY(0) rotate(1deg) scale(1);
    }
    93.3% {
      opacity: 1;
      transform: translateY(0) rotate(1deg) scale(1);
    }
    100% {
      opacity: 0;
      transform: translateY(0) rotate(1deg) scale(0.95);
    }
  }
  @keyframes clarity-flow {
    0%,
    60% {
      opacity: 0;
      transform: translateX(-50%) translateY(6px);
    }
    63.3% {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
    93.3% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }

  /* ===== RESPONSIVE ===== */
  @media (max-width: 768px) {
    .nav-links {
      display: none;
    }
    .steps {
      grid-template-columns: 1fr;
      gap: 32px;
    }
    .steps::before,
    .steps::after {
      display: none;
    }
    .feature-row {
      grid-template-columns: 1fr;
      gap: 32px;
    }
    .feature-row.reverse .feature-text {
      order: 1;
    }
    .feature-row.reverse .feature-visual {
      order: 2;
    }
    .usecases-grid {
      grid-template-columns: 1fr;
    }
    .pricing-grid {
      grid-template-columns: 1fr;
      max-width: 400px;
    }
    .footer-inner {
      flex-direction: column;
      gap: 12px;
      text-align: center;
    }
    .mockup-canvas {
      height: 340px;
    }
    .demo-root-card {
      min-width: 160px;
      max-width: 180px;
      padding: 12px 14px;
    }
    .demo-root-card .fc-emoji {
      font-size: 1.4em;
    }
    .demo-root-card .fc-text {
      font-size: 12px;
    }
    .demo-card {
      min-width: 110px;
      max-width: 130px;
      padding: 8px 10px;
    }
    .demo-card .fc-emoji {
      font-size: 1.1em;
      margin-bottom: 3px;
    }
    .demo-card .fc-text {
      font-size: 10px;
      line-height: 1.3;
    }
    .demo-card .fc-label {
      font-size: 9px;
    }
    .demo-card-1 {
      left: 2%;
      top: 12%;
    }
    .demo-card-2 {
      right: 2%;
      top: 8%;
    }
    .demo-card-3 {
      left: 0%;
      top: 60%;
    }
    .demo-card-4 {
      right: 0%;
      top: 56%;
    }
    .demo-card-5 {
      right: 0%;
      top: 34%;
    }
    .demo-voice-bar {
      font-size: 12px;
      padding: 8px 14px;
    }
    .demo-clarity {
      font-size: 16px;
      bottom: 48px;
    }
    .blindspot-cards {
      flex-direction: column;
    }
    .cta-primary {
      font-size: 14px;
      padding: 12px 24px;
    }
    .hero-actions {
      flex-direction: column;
    }
  }

  /* ===== PREFERS REDUCED MOTION ===== */
  @media (prefers-reduced-motion: reduce) {
    :global(.reveal),
    :global(.reveal-left),
    :global(.reveal-right) {
      opacity: 1;
      transform: none;
      transition: none;
    }
    .hero-title,
    .hero-subtitle,
    .hero-actions,
    .hero-mockup {
      opacity: 1;
      transform: none;
      animation: none;
    }
    .demo-root-card,
    .demo-card,
    .demo-voice-bar,
    .demo-clarity {
      animation: none;
    }
    .demo-root-card {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1);
    }
    .demo-card {
      opacity: 1;
      transform: none;
    }
    .demo-voice-bar {
      opacity: 0;
    }
    .demo-clarity {
      opacity: 1;
      transform: translateX(-50%);
    }
    .cta-primary::after {
      animation: none;
    }
  }
</style>
