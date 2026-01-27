import { writable } from 'svelte/store';
import { API_BASE } from '../config';

export interface BoardSummary {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

interface BoardsState {
  items: BoardSummary[];
  activeId: string | null;
  isLoading: boolean;
  error: string | null;
}

const { subscribe, set, update } = writable<BoardsState>({
  items: [],
  activeId: null,
  isLoading: false,
  error: null
});

async function fetchBoards(token: string) {
  update((state) => ({ ...state, isLoading: true, error: null }));
  try {
    const response = await fetch(`${API_BASE}/api/sessions`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to load sessions: ${response.status}`);
    }
    const data = await response.json();
    const items = Array.isArray(data.sessions) ? data.sessions : [];
    update((state) => ({
      ...state,
      items,
      activeId: state.activeId || (items[0]?.id ?? null),
      isLoading: false
    }));
  } catch (error) {
    update((state) => ({
      ...state,
      isLoading: false,
      error: error instanceof Error ? error.message : 'Failed to load sessions'
    }));
  }
}

async function createBoard(token: string) {
  try {
    const response = await fetch(`${API_BASE}/api/sessions`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error(`Failed to create session: ${response.status}`);
    }
    const data = await response.json();
    const session = data.session as { id: string; title?: string };
    const newBoard: BoardSummary = {
      id: session.id,
      title: session.title || 'Untitled board',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    update((state) => ({
      ...state,
      items: [newBoard, ...state.items],
      activeId: newBoard.id
    }));
    return newBoard;
  } catch (error) {
    update((state) => ({
      ...state,
      error: error instanceof Error ? error.message : 'Failed to create session'
    }));
    return null;
  }
}

function setActiveBoard(id: string) {
  update((state) => ({ ...state, activeId: id }));
}

function updateBoardTitle(id: string, title: string) {
  update((state) => ({
    ...state,
    items: state.items.map((item) => (item.id === id ? { ...item, title, updated_at: new Date().toISOString() } : item))
  }));
}

async function deleteBoard(token: string, id: string): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/api/sessions/${id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    if (response.ok) {
      update((state) => ({
        ...state,
        items: state.items.filter((b) => b.id !== id),
        activeId: state.activeId === id ? (state.items.find((b) => b.id !== id)?.id ?? null) : state.activeId
      }));
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

export const boards = {
  subscribe,
  fetchBoards,
  createBoard,
  setActiveBoard,
  updateBoardTitle,
  deleteBoard,
  reset: () =>
    set({
      items: [],
      activeId: null,
      isLoading: false,
      error: null
    })
};
