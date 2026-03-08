<script lang="ts">
  import type { AuthErrorCode } from "../stores/auth";
  import { strings } from "../stores/i18n";

  type Props = {
    error: AuthErrorCode;
    onRetry: () => void;
    onRelogin: () => void;
  };

  let { error, onRetry, onRelogin }: Props = $props();
</script>

<div class="auth-state auth-state-error">
  <div class="auth-card">
    <p class="auth-kicker">Fact Cards</p>
    <h1 class="auth-title">
      {error === "session_expired"
        ? $strings.auth?.sessionExpiredTitle || "Your session ended"
        : $strings.auth?.errorTitle || "Sign-in needs another try"}
    </h1>
    <p class="auth-copy">
      {error === "session_expired"
        ? $strings.auth?.sessionExpiredBody ||
          "Your boards are still here. Sign in again to reopen them."
        : $strings.auth?.errorBody ||
          "We could not confirm your session right now. Retry or open sign-in again."}
    </p>
    <div class="auth-actions">
      <button class="auth-btn auth-btn-primary" onclick={onRetry}>
        {$strings.auth?.retry || "Try again"}
      </button>
      <button class="auth-btn auth-btn-secondary" onclick={onRelogin}>
        {$strings.auth?.signInAgain || "Sign in again"}
      </button>
    </div>
  </div>
</div>

<style>
  .auth-state {
    width: 100%;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "DM Sans", sans-serif;
    color: var(--text-dark);
  }

  .auth-state-error {
    padding: 24px;
    background:
      radial-gradient(circle at top, rgba(255, 255, 255, 0.92), transparent 40%),
      linear-gradient(180deg, #efe5d1 0%, #f7f1e7 100%);
  }

  .auth-card {
    width: min(520px, 100%);
    padding: 28px;
    border-radius: 24px;
    border: 1px solid rgba(143, 87, 42, 0.14);
    background: rgba(255, 252, 246, 0.96);
    box-shadow: 0 22px 60px rgba(91, 53, 20, 0.12);
    text-align: center;
  }

  .auth-kicker {
    margin: 0 0 10px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(116, 71, 35, 0.72);
  }

  .auth-title {
    margin: 0;
    font-size: clamp(1.8rem, 2.4vw, 2.4rem);
    line-height: 1.1;
  }

  .auth-copy {
    margin: 14px 0 0;
    font-size: 1rem;
    line-height: 1.6;
    color: rgba(54, 39, 26, 0.82);
  }

  .auth-actions {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    margin-top: 22px;
  }

  .auth-btn {
    border: none;
    border-radius: 999px;
    padding: 12px 20px;
    font: inherit;
    font-weight: 700;
    cursor: pointer;
    transition:
      transform 0.18s ease,
      box-shadow 0.18s ease,
      background-color 0.18s ease;
  }

  .auth-btn:hover {
    transform: translateY(-1px);
  }

  .auth-btn-primary {
    background: #a44b1f;
    color: #fffdf8;
    box-shadow: 0 12px 26px rgba(164, 75, 31, 0.24);
  }

  .auth-btn-secondary {
    background: #efe4d6;
    color: #4f3521;
  }

  @media (max-width: 640px) {
    .auth-card {
      padding: 24px 20px;
    }

    .auth-actions {
      flex-direction: column;
    }

    .auth-btn {
      width: 100%;
    }
  }
</style>
