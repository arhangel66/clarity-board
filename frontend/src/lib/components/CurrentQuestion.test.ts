import { render } from '@testing-library/svelte';
import { tick } from 'svelte';
import { test, expect, afterEach, beforeEach } from 'vitest';

import CurrentQuestion from './CurrentQuestion.svelte';
import { session } from '../stores/session';
import { locale, strings } from '../stores/i18n';
import { get } from 'svelte/store';

beforeEach(() => {
  locale.set('en');
  session.reset();
});

afterEach(() => {
  session.reset();
});

test('renders the active question banner with default question', () => {
  const { getByText } = render(CurrentQuestion);
  const copy = get(strings);

  expect(getByText(copy.session.defaultQuestions.question.question)).toBeInTheDocument();
  expect(getByText(copy.session.phaseLabels.question)).toBeInTheDocument();
});

test('shows thinking indicator when AI is thinking', async () => {
  const { container } = render(CurrentQuestion);

  session.setThinking(true);
  await tick();

  expect(container.querySelector('.thinking-dots')).toBeInTheDocument();
});
