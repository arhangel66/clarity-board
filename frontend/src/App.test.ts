import { render } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
// @ts-ignore
import App from './App.svelte';

describe('App', () => {
    it('renders without crashing', () => {
        // Basic smoke test
        const { container } = render(App);
        expect(container).toBeTruthy();
    });
});
