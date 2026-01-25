<script lang="ts">
  import { onMount } from 'svelte';
  import { auth } from '../stores/auth';
  import { strings } from '../stores/i18n';

  function handleLogin() {
    auth.loginWithGoogle();
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

<section class="landing">
  <div class="landing-hero">
    <div class="hero-copy">
      <div class="hero-kicker">Fact Cards</div>
      <h1 class="hero-title">{$strings.landing.title}</h1>
      <p class="hero-subtitle">{$strings.landing.subtitle}</p>
      <div class="hero-story">
        <h2>{$strings.landing.storyTitle}</h2>
        <p>{$strings.landing.story}</p>
        <p class="hero-payoff">{$strings.landing.payoff}</p>
      </div>
      <ul class="hero-steps">
        {#each $strings.landing.steps as step}
          <li>{step}</li>
        {/each}
      </ul>
      <button class="cta-btn" onclick={handleLogin}>{$strings.landing.cta}</button>
      <div class="cta-note">{$strings.landing.note}</div>
    </div>
    <div class="hero-visual">
      <div class="card-stack">
        <div class="sample-card card-a">
          <div class="card-top"></div>
          <div class="card-text">"{$strings.session.defaultQuestions.question.question}"</div>
        </div>
        <div class="sample-card card-b">
          <div class="card-top"></div>
          <div class="card-text">{$strings.landing.samples[1]}</div>
        </div>
        <div class="sample-card card-c">
          <div class="card-top"></div>
          <div class="card-text">{$strings.landing.samples[2]}</div>
        </div>
        <div class="sample-card card-d">
          <div class="card-top"></div>
          <div class="card-text">{$strings.landing.samples[3]}</div>
        </div>
      </div>
      <div class="hero-grid"></div>
    </div>
  </div>
</section>

<style>
  :global(html.landing-active, body.landing-active) {
    height: auto;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
  }

  :global(body.landing-active #app) {
    min-height: 100%;
    height: auto;
  }

  .landing {
    min-height: 100vh;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at top left, #f6efe4 0%, #f2e2cd 45%, #e5cfb2 100%);
    position: relative;
    overflow: hidden;
  }

  .landing::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.6), transparent 40%),
      radial-gradient(circle at 80% 10%, rgba(255, 255, 255, 0.4), transparent 45%),
      radial-gradient(circle at 30% 80%, rgba(255, 255, 255, 0.3), transparent 40%);
    pointer-events: none;
  }

  .landing-hero {
    position: relative;
    display: grid;
    grid-template-columns: minmax(320px, 1.1fr) minmax(280px, 0.9fr);
    gap: 48px;
    max-width: 1100px;
    padding: 60px 40px;
    z-index: 1;
  }

  .hero-copy {
    display: flex;
    flex-direction: column;
    gap: 20px;
    color: #2f2a24;
  }

  .hero-kicker {
    font-family: "Caveat", cursive;
    font-size: 1.4em;
    color: #9a6b3f;
    letter-spacing: 0.05em;
  }

  .hero-title {
    font-family: "Fraunces", serif;
    font-size: clamp(2.4rem, 3vw, 3.4rem);
    line-height: 1.05;
  }

  .hero-subtitle {
    font-family: "DM Sans", sans-serif;
    font-size: 1.05em;
    color: #4f463b;
  }

  .hero-story {
    padding: 20px 22px;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.65);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  }

  .hero-story h2 {
    font-family: "Fraunces", serif;
    font-size: 1.1em;
    margin-bottom: 8px;
  }

  .hero-story p {
    font-family: "DM Sans", sans-serif;
    font-size: 0.95em;
    color: #4b4339;
  }

  .hero-payoff {
    margin-top: 10px;
    font-weight: 600;
  }

  .hero-steps {
    list-style: none;
    display: grid;
    gap: 10px;
    font-family: "DM Sans", sans-serif;
    font-size: 0.95em;
  }

  .hero-steps li {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .hero-steps li::before {
    content: '';
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #9a6b3f;
  }

  .cta-btn {
    align-self: flex-start;
    padding: 12px 22px;
    border-radius: 999px;
    border: none;
    background: #2f2a24;
    color: #fffdf7;
    font-family: "DM Sans", sans-serif;
    font-size: 0.95em;
    cursor: pointer;
    box-shadow: 0 12px 24px rgba(47, 42, 36, 0.25);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .cta-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 16px 28px rgba(47, 42, 36, 0.3);
  }

  .cta-note {
    font-size: 0.8em;
    color: #6a5f52;
  }

  .hero-visual {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .card-stack {
    position: relative;
    width: 100%;
    max-width: 320px;
    height: 360px;
  }

  .sample-card {
    position: absolute;
    padding: 18px 20px 26px;
    border-radius: 10px;
    background: #fffdf8;
    box-shadow: 0 18px 32px rgba(0, 0, 0, 0.18);
    font-family: "DM Sans", sans-serif;
    color: #2f2a24;
    line-height: 1.3;
  }

  .card-top {
    height: 6px;
    width: 100%;
    border-radius: 6px;
    background: #9a6b3f;
    margin-bottom: 10px;
  }

  .card-a {
    width: 90%;
    top: 0;
    left: 10%;
    transform: rotate(-4deg);
  }

  .card-b {
    width: 88%;
    top: 80px;
    left: 0;
    transform: rotate(5deg);
    background: #fdf3e7;
  }

  .card-c {
    width: 86%;
    top: 180px;
    left: 14%;
    transform: rotate(-2deg);
    background: #f8fafc;
  }

  .card-d {
    width: 70%;
    top: 260px;
    left: 8%;
    transform: rotate(8deg);
    background: #e6f8f5;
  }

  .hero-grid {
    position: absolute;
    inset: -20px;
    border-radius: 24px;
    background: repeating-linear-gradient(
      90deg,
      rgba(255, 255, 255, 0.2) 0,
      rgba(255, 255, 255, 0.2) 1px,
      transparent 1px,
      transparent 18px
    ),
      repeating-linear-gradient(
        0deg,
        rgba(255, 255, 255, 0.2) 0,
        rgba(255, 255, 255, 0.2) 1px,
        transparent 1px,
        transparent 18px
      );
    z-index: -1;
  }

  @media (max-width: 900px) {
    .landing-hero {
      grid-template-columns: 1fr;
    }

    .hero-visual {
      order: -1;
    }
  }

  @media (max-width: 600px) {
    .landing-hero {
      padding: 40px 24px;
    }

    .hero-title {
      font-size: 2.2rem;
    }
  }

  @media (max-width: 360px) {
    .landing-hero {
      padding: 32px 18px;
    }

    .hero-title {
      font-size: 2rem;
    }
  }
</style>
