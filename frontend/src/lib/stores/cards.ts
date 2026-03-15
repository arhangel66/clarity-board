import { derived, get, writable } from 'svelte/store';
import type { Card, Connection, ChatMessage } from '../types';
import { locale, translations } from './i18n';
import type { Locale } from './i18n';

const CARD_MIN_DISTANCE = 14;
const CARD_BOUNDS = { min: 5, max: 95 };

function clampPercent(value: number): number {
  return Math.max(CARD_BOUNDS.min, Math.min(CARD_BOUNDS.max, value));
}

function isPositionOccupied(x: number, y: number, positions: { x: number; y: number }[]): boolean {
  return positions.some((pos) => Math.hypot(pos.x - x, pos.y - y) < CARD_MIN_DISTANCE);
}

function findFreePosition(
  x: number,
  y: number,
  occupied: { x: number; y: number }[]
): { x: number; y: number; moved: boolean } {
  const startX = clampPercent(x);
  const startY = clampPercent(y);
  const wasOccupied = isPositionOccupied(startX, startY, occupied);
  if (!wasOccupied) {
    return { x: startX, y: startY, moved: startX !== x || startY !== y };
  }

  const step = 6;
  const maxRadius = 42;
  const angleStep = 30;

  for (let radius = step; radius <= maxRadius; radius += step) {
    for (let angle = 0; angle < 360; angle += angleStep) {
      const rad = (angle * Math.PI) / 180;
      const candidateX = clampPercent(startX + Math.cos(rad) * radius);
      const candidateY = clampPercent(startY + Math.sin(rad) * radius);
      if (!isPositionOccupied(candidateX, candidateY, occupied)) {
        return { x: candidateX, y: candidateY, moved: true };
      }
    }
  }

  console.warn('[cards] No free slot found; using crowded position', {
    x: startX,
    y: startY
  });
  return { x: startX, y: startY, moved: false };
}

function createCardsStore() {
  const { subscribe, set, update } = writable<Card[]>([]);

  return {
    subscribe,
    set,
    addCards: (newCards: Card[]) => {
      const adjusted: { id: string; x: number; y: number }[] = [];
      update((existing) => {
        const existingIds = new Set(existing.map((c) => c.id));
        const occupied = existing.map((card) => ({ x: card.x, y: card.y }));
        // Convert coordinates from 0-1 (backend) to 0-100 (frontend percentage)
        // Add default values for optional fields
        const cardsToAdd = newCards
          .filter((c) => !existingIds.has(c.id))
          .map((c) => {
            const baseX = c.x * 100;
            const baseY = c.y * 100;
            if (c.is_root || c.pinned) {
              occupied.push({ x: baseX, y: baseY });
              return {
                ...c,
                x: baseX,
                y: baseY,
                target_x: (c.target_x ?? c.x) * 100,
                target_y: (c.target_y ?? c.y) * 100,
                is_new: c.is_new ?? true
              };
            }

            const resolved = findFreePosition(baseX, baseY, occupied);
            occupied.push({ x: resolved.x, y: resolved.y });
            if (resolved.moved) {
              adjusted.push({ id: c.id, x: resolved.x, y: resolved.y });
            }
            return {
              ...c,
              x: resolved.x,
              y: resolved.y,
              target_x: resolved.x,
              target_y: resolved.y,
              is_new: c.is_new ?? true
            };
          });
        return [...existing, ...cardsToAdd];
      });
      return adjusted;
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
            return { ...card, ...converted, is_updated: true };
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
    clearUpdatedFlag: (id: string) => {
      update((cards) => {
        return cards.map((card) => {
          if (card.id === id) {
            return { ...card, is_updated: false };
          }
          return card;
        });
      });
    },
    deleteCard: (id: string) => {
      update((cards) => cards.filter((c) => c.id !== id));
    },
    markDeleting: (id: string) => {
      update((cards) => {
        return cards.map((card) => {
          if (card.id === id) {
            return { ...card, is_deleting: true };
          }
          return card;
        });
      });
    },
    deleteCards: (ids: string[]) => {
      const idsSet = new Set(ids);
      update((cards) => cards.filter((c) => !idsSet.has(c.id)));
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
    deleteConnection: (id: string) => {
      update((connections) => connections.filter((c) => c.id !== id));
    },
    clear: () => set([])
  };
}

function createChatStore() {
  const initialLocale = get(locale);
  const initialWelcome = translations[initialLocale].chat.welcome;
  const { subscribe, set, update } = writable<ChatMessage[]>([
    {
      id: 'welcome',
      text: initialWelcome,
      sender: 'system',
      timestamp: new Date()
    }
  ]);
  let activeLocale: Locale = initialLocale;

  locale.subscribe((nextLocale) => {
    update((messages) => {
      if (nextLocale === activeLocale) return messages;
      const previousWelcome = translations[activeLocale].chat.welcome;
      const nextWelcome = translations[nextLocale].chat.welcome;
      activeLocale = nextLocale;
      if (
        messages.length === 1 &&
        messages[0]?.id === 'welcome' &&
        messages[0].text === previousWelcome
      ) {
        return [{ ...messages[0], text: nextWelcome }];
      }
      return messages;
    });
  });

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
          text: translations[activeLocale].chat.welcome,
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
