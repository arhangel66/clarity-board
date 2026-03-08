import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import PaywallModal from './PaywallModal.svelte';
import { access } from '../stores/access';
import { setLocale } from '../stores/i18n';
import type { AccessSnapshot } from '../types';

function buildSnapshot(status: AccessSnapshot['status']): AccessSnapshot {
  return {
    contract: {
      status_endpoint: '/api/access',
      pricing_unit: 'sessions',
      free_sessions_total: 3,
      session_consumption_trigger: 'first_ai_message_on_blank_session',
      blank_session_consumes: false,
      reopen_existing_session_consumes: false,
      deleting_session_restores_quota: false,
      supported_plans: ['free', 'monthly', 'lifetime'],
      monthly_requires_expires_at: true,
      lifetime_never_expires: true,
    },
    status,
  };
}

describe('PaywallModal', () => {
  beforeEach(() => {
    access.reset();
    setLocale('en');
  });

  afterEach(() => {
    cleanup();
    access.reset();
    setLocale('en');
  });

  it('opens automatically when starter access is exhausted', () => {
    access.hydrate(
      buildSnapshot({
        plan: 'free',
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: 'tracked',
      }),
    );

    render(PaywallModal);

    expect(
      screen.getByRole('dialog', { name: /you've used your 3 free sessions/i }),
    ).toBeInTheDocument();
    expect(screen.getByText('Starter')).toBeInTheDocument();
    expect(screen.getByText('Unlimited')).toBeInTheDocument();
    expect(screen.getByText('Lifetime')).toBeInTheDocument();
    expect(screen.getByText('$10')).toBeInTheDocument();
    expect(screen.getByText('$100')).toBeInTheDocument();
    expect(screen.getByText(/billing is not live yet/i)).toBeInTheDocument();
  });

  it('stays hidden while starter sessions remain', () => {
    access.hydrate(
      buildSnapshot({
        plan: 'free',
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 1,
        free_sessions_remaining: 2,
        can_start_ai_session: true,
        metering_state: 'tracked',
      }),
    );

    render(PaywallModal);

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('can be dismissed for the current exhausted state', async () => {
    access.hydrate(
      buildSnapshot({
        plan: 'free',
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: 'tracked',
      }),
    );

    render(PaywallModal);

    await fireEvent.click(
      screen.getByLabelText(/close upgrade preview/i, { selector: '.paywall-close' }),
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('tracks upgrade clicks with the selected plan and paywall surface', async () => {
    const ym = vi.fn();
    window.ym = ym;

    access.hydrate(
      buildSnapshot({
        plan: 'free',
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: 'tracked',
      }),
    );

    render(PaywallModal);

    await fireEvent.click(screen.getByRole('button', { name: 'Choose Monthly' }));

    expect(ym).toHaveBeenCalledWith(107194444, 'reachGoal', 'upgrade_clicked', {
      plan: 'monthly',
      surface: 'paywall_modal',
    });
    expect(screen.getByText(/checkout opens in a later release/i)).toBeInTheDocument();
  });
});
