<script lang="ts">
  import { strings } from "../stores/i18n";
  import { boards } from "../stores/boards";
  import { auth } from "../stores/auth";

  let authToken = $state<string | null>(null);

  $effect(() => {
    const unsubscribe = auth.subscribe((state) => {
      authToken = state.token;
    });
    return unsubscribe;
  });

  async function handleNewBoard() {
    if (!authToken) return;
    await boards.createBoard(authToken);
  }
</script>

<div class="demo-banner">
  <span class="demo-text">{$strings.demo.banner}</span>
  <button class="demo-cta" onclick={handleNewBoard}>
    {$strings.demo.newBoard}
  </button>
</div>

<style>
  .demo-banner {
    position: fixed;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 110;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 20px;
    background: rgba(243, 237, 255, 0.95);
    backdrop-filter: blur(12px);
    border: 2px dashed rgba(149, 117, 205, 0.4);
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(149, 117, 205, 0.15);
    animation: slideDown 0.4s ease-out;
  }

  .demo-text {
    font-size: 0.9em;
    color: var(--text-dark);
    font-weight: 500;
  }

  .demo-cta {
    border: none;
    padding: 8px 16px;
    border-radius: 12px;
    background: var(--question-purple);
    color: white;
    font-size: 0.85em;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(149, 117, 205, 0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .demo-cta:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(149, 117, 205, 0.4);
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  @media (max-width: 600px) {
    .demo-banner {
      left: 8px;
      right: 8px;
      transform: none;
      flex-direction: column;
      text-align: center;
      gap: 10px;
    }

    @keyframes slideDown {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  }
</style>
