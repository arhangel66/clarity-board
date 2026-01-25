<script lang="ts">
  import { boards } from '../stores/boards';
  import { auth } from '../stores/auth';
  import { strings } from '../stores/i18n';

  let authToken: string | null = null;
  let userName = '';

  $effect(() => {
    const unsubscribe = auth.subscribe((state) => {
      authToken = state.token;
      userName = state.user?.name || state.user?.email || 'User';
    });
    return unsubscribe;
  });

  function selectBoard(boardId: string) {
    boards.setActiveBoard(boardId);
  }

  async function createBoard() {
    if (!authToken) return;
    await boards.createBoard(authToken);
  }
</script>

<aside class="boards-sidebar">
  <div class="sidebar-header">
    <div class="app-name">Fact Cards</div>
    <button class="new-board-btn" onclick={createBoard}>
      {$strings.sidebar?.newBoard || 'New board'}
    </button>
  </div>

  <div class="boards-section">
    <div class="section-title">{$strings.sidebar?.boards || 'Boards'}</div>
    {#if $boards.isLoading}
      <div class="boards-loading">{$strings.sidebar?.loading || 'Loading...'}</div>
    {:else}
      <div class="boards-list">
        {#each $boards.items as board (board.id)}
          <button
            class="board-item"
            class:active={$boards.activeId === board.id}
            onclick={() => selectBoard(board.id)}
          >
            <div class="board-title">{board.title}</div>
            <div class="board-meta">{new Date(board.updated_at).toLocaleDateString()}</div>
          </button>
        {/each}
        {#if $boards.items.length === 0}
          <div class="boards-empty">{$strings.sidebar?.empty || 'No boards yet'}</div>
        {/if}
      </div>
    {/if}
  </div>

  <div class="sidebar-footer">
    <div class="user-info">
      <div class="user-name">{userName}</div>
      <button class="logout-btn" onclick={() => auth.logout()}>
        {$strings.sidebar?.logout || 'Logout'}
      </button>
    </div>
  </div>
</aside>

<style>
  .boards-sidebar {
    width: 260px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: linear-gradient(180deg, #f9f5ef 0%, #f0e7da 100%);
    border-right: 1px solid rgba(0, 0, 0, 0.05);
    padding: 20px 16px;
    box-shadow: 8px 0 24px rgba(0, 0, 0, 0.08);
    z-index: 120;
  }

  .sidebar-header {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 18px;
  }

  .app-name {
    font-family: "Caveat", cursive;
    font-size: 1.6em;
    color: var(--text-dark);
  }

  .new-board-btn {
    border: none;
    padding: 8px 12px;
    border-radius: 12px;
    background: var(--question-purple);
    color: white;
    font-size: 0.85em;
    cursor: pointer;
    box-shadow: 0 6px 16px rgba(149, 117, 205, 0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .new-board-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(149, 117, 205, 0.35);
  }

  .boards-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .section-title {
    font-size: 0.75em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-light);
  }

  .boards-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
    padding-right: 4px;
  }

  .board-item {
    border: none;
    text-align: left;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .board-item:hover {
    transform: translateY(-1px);
    background: rgba(255, 255, 255, 0.95);
  }

  .board-item.active {
    background: rgba(149, 117, 205, 0.16);
    border: 1px solid rgba(149, 117, 205, 0.4);
  }

  .board-title {
    font-size: 0.9em;
    color: var(--text-dark);
  }

  .board-meta {
    font-size: 0.7em;
    color: var(--text-light);
    margin-top: 4px;
  }

  .boards-loading,
  .boards-empty {
    font-size: 0.85em;
    color: var(--text-medium);
  }

  .sidebar-footer {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
  }

  .user-info {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .user-name {
    font-size: 0.85em;
    color: var(--text-dark);
  }

  .logout-btn {
    border: none;
    background: transparent;
    color: var(--text-light);
    cursor: pointer;
    font-size: 0.8em;
  }

  @media (max-width: 900px) {
    .boards-sidebar {
      display: none;
    }
  }
</style>
