import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/svelte";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import PaywallModal from "./PaywallModal.svelte";
import { access } from "../stores/access";
import { setLocale } from "../stores/i18n";
import type { AccessSnapshot } from "../types";

function buildSnapshot(status: AccessSnapshot["status"]): AccessSnapshot {
  return {
    contract: {
      status_endpoint: "/api/access",
      pricing_unit: "sessions",
      free_sessions_total: 3,
      session_consumption_trigger: "first_ai_message_on_blank_session",
      blank_session_consumes: false,
      reopen_existing_session_consumes: false,
      deleting_session_restores_quota: false,
      supported_plans: ["free", "monthly", "lifetime"],
      monthly_requires_expires_at: true,
      lifetime_never_expires: true,
    },
    status,
  };
}

function renderPaywall() {
  return render(PaywallModal, {
    props: {
      viewerId: "user-1",
    },
  });
}

describe("PaywallModal", () => {
  beforeEach(() => {
    access.reset();
    window.sessionStorage.clear();
    setLocale("en");
  });

  afterEach(() => {
    cleanup();
    access.reset();
    window.sessionStorage.clear();
    setLocale("en");
  });

  it("opens automatically when starter access is exhausted", () => {
    access.hydrate(
      buildSnapshot({
        plan: "free",
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: "tracked",
      }),
    );

    renderPaywall();

    expect(
      screen.getByRole("dialog", { name: /you've used your 3 free sessions/i }),
    ).toBeInTheDocument();
    expect(screen.getByText("Starter")).toBeInTheDocument();
    expect(screen.getByText("Unlimited")).toBeInTheDocument();
    expect(screen.getByText("Lifetime")).toBeInTheDocument();
    expect(screen.getByText("$10")).toBeInTheDocument();
    expect(screen.getByText("$100")).toBeInTheDocument();
    expect(screen.getByText(/payment is not live yet/i)).toBeInTheDocument();
  });

  it("stays hidden while starter sessions remain", () => {
    access.hydrate(
      buildSnapshot({
        plan: "free",
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 1,
        free_sessions_remaining: 2,
        can_start_ai_session: true,
        metering_state: "tracked",
      }),
    );

    renderPaywall();

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("can be dismissed for the current exhausted state", async () => {
    access.hydrate(
      buildSnapshot({
        plan: "free",
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: "tracked",
      }),
    );

    renderPaywall();

    await fireEvent.click(
      screen.getByLabelText(/close upgrade preview/i, { selector: ".paywall-close" }),
    );

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("stays closed after remount while the same exhausted state persists", async () => {
    access.hydrate(
      buildSnapshot({
        plan: "free",
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: "tracked",
      }),
    );

    renderPaywall();

    await fireEvent.click(
      screen.getByLabelText(/close upgrade preview/i, { selector: ".paywall-close" }),
    );

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    cleanup();
    renderPaywall();

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("reopens after a later blocked action for the same exhausted state", async () => {
    access.hydrate(
      buildSnapshot({
        plan: "free",
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: "tracked",
      }),
    );

    renderPaywall();

    await fireEvent.click(
      screen.getByLabelText(/close upgrade preview/i, { selector: ".paywall-close" }),
    );

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    access.requestPaywallPrompt();

    await waitFor(() => {
      expect(
        screen.getByRole("dialog", { name: /you've used your 3 free sessions/i }),
      ).toBeInTheDocument();
    });
  });

  it("tracks upgrade clicks with the selected plan and paywall surface", async () => {
    const ym = vi.fn();
    window.ym = ym;

    access.hydrate(
      buildSnapshot({
        plan: "free",
        plan_expires_at: null,
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: 3,
        free_sessions_remaining: 0,
        can_start_ai_session: false,
        metering_state: "tracked",
      }),
    );

    renderPaywall();

    await fireEvent.click(screen.getByRole("button", { name: "Choose Monthly" }));

    expect(ym).toHaveBeenCalledWith(107194444, "reachGoal", "upgrade_clicked", {
      plan: "monthly",
      surface: "paywall_modal",
    });
    expect(screen.getAllByText(/payment is not live yet/i)).toHaveLength(2);
  });
});
