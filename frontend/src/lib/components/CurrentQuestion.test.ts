import { fireEvent, render } from '@testing-library/svelte';
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

test('shows the localized category label for a pending special question', async () => {
  const { container, getByText } = render(CurrentQuestion);

  session.setPendingSpecialQuestion({
    id: 'reflector:1',
    category_id: 'reflector',
    category_label: 'Perspective',
    question: 'What observable result would show that this problem is truly solved?',
    hint: 'Describe concrete signs.'
  });
  await tick();

  const specialButton = container.querySelector('.toggle-btn.special');
  expect(specialButton).toBeInTheDocument();

  await fireEvent.click(specialButton!);

  expect(container.querySelector('.special-category')).toHaveTextContent('Perspective');
  expect(getByText('What observable result would show that this problem is truly solved?')).toBeInTheDocument();
});

test('falls back to i18n category names when the prompt has no category label', async () => {
  const { container, getByText } = render(CurrentQuestion);

  session.setPendingSpecialQuestion({
    id: 'centrist:1',
    category_id: 'centrist',
    question: 'Which external factors could sharply reshape the situation even if you do everything right?',
    hint: ''
  });
  await tick();

  const specialButton = container.querySelector('.toggle-btn.special');
  expect(specialButton).toBeInTheDocument();

  await fireEvent.click(specialButton!);

  expect(container.querySelector('.special-category')).toHaveTextContent('Context');
  expect(
    getByText('Which external factors could sharply reshape the situation even if you do everything right?')
  ).toBeInTheDocument();
});
