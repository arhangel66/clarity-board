import { describe, it, expect, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { cards } from './cards';
import type { Card } from '../types';

describe('cards store', () => {
  beforeEach(() => {
    cards.set([]);
  });

  it('adjusts positions to avoid overlap for new cards', () => {
    const existing: Card = {
      id: 'card_existing',
      text: 'Existing',
      type: 'fact',
      emoji: '',
      color: '#000',
      importance: 0.5,
      confidence: 0.8,
      x: 50,
      y: 50,
      pinned: false
    };

    cards.set([existing]);

    const incoming: Card = {
      id: 'card_new',
      text: 'New',
      type: 'fact',
      emoji: '',
      color: '#000',
      importance: 0.5,
      confidence: 0.8,
      x: 0.5,
      y: 0.5,
      pinned: false
    };

    const adjusted = cards.addCards([incoming]);
    const stored = get(cards).find((card) => card.id === 'card_new');

    expect(adjusted.length).toBe(1);
    expect(stored).toBeTruthy();
    // Position should differ from existing card (at least one coordinate changed)
    const positionChanged = stored?.x !== 50 || stored?.y !== 50;
    expect(positionChanged).toBe(true);
  });

  it('keeps pinned cards at provided position', () => {
    const existing: Card = {
      id: 'card_existing',
      text: 'Existing',
      type: 'fact',
      emoji: '',
      color: '#000',
      importance: 0.5,
      confidence: 0.8,
      x: 50,
      y: 50,
      pinned: false
    };

    cards.set([existing]);

    const incoming: Card = {
      id: 'card_pinned',
      text: 'Pinned',
      type: 'fact',
      emoji: '',
      color: '#000',
      importance: 0.5,
      confidence: 0.8,
      x: 0.5,
      y: 0.5,
      pinned: true
    };

    const adjusted = cards.addCards([incoming]);
    const stored = get(cards).find((card) => card.id === 'card_pinned');

    expect(adjusted.length).toBe(0);
    expect(stored?.x).toBe(50);
    expect(stored?.y).toBe(50);
  });
});
