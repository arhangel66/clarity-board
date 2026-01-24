import { render } from '@testing-library/svelte';
import { describe, it, expect, beforeEach } from 'vitest';
import Connections from './Connections.svelte';
import { cards, connections } from '../stores/cards';
import type { Card } from '../types';

describe('Connections', () => {
    beforeEach(() => {
        cards.set([]);
        connections.set([]);
    });

    it('renders nothing when no connections', () => {
        const { container } = render(Connections);
        expect(container.querySelector('path')).not.toBeInTheDocument();
    });

    it('renders a line between two cards', async () => {
        const cardA: Card = {
            id: '1', text: 'A', type: 'fact', emoji: '🔍', color: 'blue',
            importance: 1, confidence: 1, x: 0.1, y: 0.1, pinned: false
        };
        const cardB: Card = {
            id: '2', text: 'B', type: 'fact', emoji: '💡', color: 'blue',
            importance: 1, confidence: 1, x: 0.5, y: 0.5, pinned: false
        };

        cards.set([cardA, cardB]);

        connections.set([
            { id: 'c1', from_id: '1', to_id: '2', type: 'causes', strength: 1, label: null, created_by: 'user' }
        ]);

        const { container } = render(Connections);
        expect(container.querySelector('path')).toBeInTheDocument();
    });
});
