import { writable, derived } from 'svelte/store';
import type { Card, Connection, ChatMessage } from '../types';

function createCardsStore() {
  const { subscribe, set, update } = writable<Card[]>([]);

  return {
    subscribe,
    set,
    addCards: (newCards: Card[]) => {
      update((existing) => {
        const existingIds = new Set(existing.map((c) => c.id));
        // Convert coordinates from 0-1 (backend) to 0-100 (frontend percentage)
        const cardsToAdd = newCards
          .filter((c) => !existingIds.has(c.id))
          .map((c) => ({
            ...c,
            x: c.x * 100,
            y: c.y * 100,
            target_x: c.target_x * 100,
            target_y: c.target_y * 100
          }));
        return [...existing, ...cardsToAdd];
      });
    },
    updateCards: (updates: Partial<Card>[]) => {
      update((cards) => {
        return cards.map((card) => {
          const cardUpdate = updates.find((u) => u.id === card.id);
          if (cardUpdate) {
            // Convert coordinates from 0-1 (backend) to 0-100 (frontend) if present
            const converted = { ...cardUpdate };
            if (converted.x !== undefined) converted.x = converted.x * 100;
            if (converted.y !== undefined) converted.y = converted.y * 100;
            if (converted.target_x !== undefined) converted.target_x = converted.target_x * 100;
            if (converted.target_y !== undefined) converted.target_y = converted.target_y * 100;
            return { ...card, ...converted };
          }
          return card;
        });
      });
    },
    updateCard: (id: string, changes: Partial<Card>) => {
      update((cards) => {
        return cards.map((card) => {
          if (card.id === id) {
            return { ...card, ...changes };
          }
          return card;
        });
      });
    },
    updatePositions: (positions: { id: string; target_x: number; target_y: number }[]) => {
      update((cards) => {
        return cards.map((card) => {
          const pos = positions.find((p) => p.id === card.id);
          if (pos) {
            // Convert from 0-1 (backend) to 0-100 (frontend)
            return { ...card, target_x: pos.target_x * 100, target_y: pos.target_y * 100 };
          }
          return card;
        });
      });
    },
    clearNewFlag: (id: string) => {
      update((cards) => {
        return cards.map((card) => {
          if (card.id === id) {
            return { ...card, is_new: false };
          }
          return card;
        });
      });
    },
    clear: () => set([])
  };
}

function createConnectionsStore() {
  const { subscribe, set, update } = writable<Connection[]>([]);

  return {
    subscribe,
    set,
    addConnections: (connections: Connection[]) => {
      update((existing) => {
        const existingIds = new Set(existing.map((c) => c.id));
        const newConnections = connections.filter((c) => !existingIds.has(c.id));
        return [...existing, ...newConnections];
      });
    },
    clear: () => set([])
  };
}

function createChatStore() {
  const { subscribe, set, update } = writable<ChatMessage[]>([
    {
      id: 'welcome',
      text: 'Welcome to Fact Cards. Describe the problem you want to analyze.',
      sender: 'system',
      timestamp: new Date()
    }
  ]);

  return {
    subscribe,
    set,
    addMessage: (text: string, sender: 'user' | 'system' | 'ai') => {
      update((messages) => [
        ...messages,
        {
          id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          text,
          sender,
          timestamp: new Date()
        }
      ]);
    },
    clear: () =>
      set([
        {
          id: 'welcome',
          text: 'Welcome to Fact Cards. Describe the problem you want to analyze.',
          sender: 'system',
          timestamp: new Date()
        }
      ])
  };
}

export const cards = createCardsStore();
export const connections = createConnectionsStore();
export const chatMessages = createChatStore();

// Derived store for card lookup by ID
export const cardsById = derived(cards, ($cards) => {
  const map = new Map<string, Card>();
  for (const card of $cards) {
    map.set(card.id, card);
  }
  return map;
});
