import { cleanup, fireEvent, render, screen } from "@testing-library/svelte";
import { get } from "svelte/store";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import BoardsSidebar from "./BoardsSidebar.svelte";
import { boards } from "../stores/boards";
import { cards } from "../stores/cards";
import { access } from "../stores/access";
import { selectedCardIds } from "../stores/selection";
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

describe("BoardsSidebar", () => {
  beforeEach(() => {
    access.reset();
    boards.reset();
    cards.clear();
    selectedCardIds.clear();
    setLocale("en");
  });

  afterEach(() => {
    cleanup();
    access.reset();
    boards.reset();
    cards.clear();
    selectedCardIds.clear();
    setLocale("en");
  });

  it("shows remaining starter sessions without credits language", () => {
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

    render(BoardsSidebar);

    expect(screen.getByText("Starter access")).toBeInTheDocument();
    expect(screen.queryByText(/credit/i)).not.toBeInTheDocument();
  });

  it("shows active paid-plan status for monthly access", () => {
    access.hydrate(
      buildSnapshot({
        plan: "monthly",
        plan_expires_at: "2026-04-07T12:00:00+00:00",
        plan_active: true,
        free_sessions_total: 3,
        free_sessions_used: null,
        free_sessions_remaining: null,
        can_start_ai_session: true,
        metering_state: "tracked",
      }),
    );

    render(BoardsSidebar);

    expect(screen.getByText("Monthly plan")).toBeInTheDocument();
  });

  it("shows paywall guidance when starter sessions exhausted", () => {
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

    render(BoardsSidebar);

    expect(screen.getByText("Starter sessions used up")).toBeInTheDocument();
    expect(
      screen.getByText(/first AI message on a blank board is blocked until you upgrade/i),
    ).toBeInTheDocument();
  });

  it("reopens the upgrade prompt from exhausted new-board guidance", async () => {
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

    render(BoardsSidebar);

    await fireEvent.click(screen.getByRole("button", { name: "View plans" }));

    expect(get(access).paywallPromptCount).toBe(1);
  });
});
