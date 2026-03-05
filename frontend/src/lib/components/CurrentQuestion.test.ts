import { render } from '@testing-library/svelte';
import { tick } from 'svelte';
import { test, expect, afterEach, beforeEach } from 'vitest';

import CurrentQuestion from './CurrentQuestion.svelte';
import { session } from '../stores/session';
import { locale } from '../stores/i18n';

beforeEach(() => {
  locale.set('en');
  session.reset();
});

afterEach(() => {
  session.reset();
});

test('renders the toggle bar with special question button', () => {
  const { container } = render(CurrentQuestion);

  // UI shows toggle bar with buttons
  expect(container.querySelector('.toggle-bar')).toBeInTheDocument();
  expect(container.querySelector('.toggle-btn.special')).toBeInTheDocument();
});

test('shows thinking indicator when AI is thinking', async () => {
  const { container } = render(CurrentQuestion);

  session.setThinking(true);
  await tick();

  expect(container.querySelector('.thinking-dots')).toBeInTheDocument();
});
