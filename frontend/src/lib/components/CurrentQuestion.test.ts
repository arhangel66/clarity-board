import { render } from '@testing-library/svelte';
import { tick } from 'svelte';
import { test, expect, afterEach } from 'vitest';

import CurrentQuestion from './CurrentQuestion.svelte';
import { session, PHASE_LABELS } from '../stores/session';

afterEach(() => {
  session.reset();
});

test('renders the active question banner with default question', () => {
  const { getByText } = render(CurrentQuestion);

  expect(getByText('State the problem in one sentence.')).toBeInTheDocument();
  expect(getByText(PHASE_LABELS.question)).toBeInTheDocument();
});

test('shows thinking indicator when AI is thinking', async () => {
  const { container } = render(CurrentQuestion);

  session.setThinking(true);
  await tick();

  expect(container.querySelector('.thinking-dots')).toBeInTheDocument();
});
