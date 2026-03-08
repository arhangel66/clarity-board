import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  reachGoal,
  trackCardCreated,
  trackConnectionCreated,
  trackLandingView,
  trackPhaseChanged,
  trackSessionCompleted,
  trackSessionExported,
  trackSignUp,
  trackSpecialQuestionUsed,
  trackUpgradeClicked,
  trackTextInput,
  trackVoiceInput,
} from "./analytics";

describe("analytics", () => {
  beforeEach(() => {
    delete window.ym;
    vi.restoreAllMocks();
  });

  it("does nothing when ym is unavailable", () => {
    expect(() => reachGoal("landing_view")).not.toThrow();
  });

  it("sends funnel goals to the configured counter", () => {
    const ym = vi.fn();
    window.ym = ym;

    trackLandingView();
    trackSignUp();
    trackSessionCompleted();

    expect(ym).toHaveBeenNthCalledWith(1, 107194444, "reachGoal", "landing_view", undefined);
    expect(ym).toHaveBeenNthCalledWith(2, 107194444, "reachGoal", "sign_up", undefined);
    expect(ym).toHaveBeenNthCalledWith(
      3,
      107194444,
      "reachGoal",
      "session_completed",
      undefined,
    );
  });

  it("sends custom event payloads without card content", () => {
    const ym = vi.fn();
    window.ym = ym;

    trackCardCreated("fact");
    trackConnectionCreated("relates");
    trackPhaseChanged("connections");
    trackSpecialQuestionUsed();
    trackSessionExported("image");
    trackVoiceInput();
    trackTextInput();
    trackUpgradeClicked("monthly", "paywall_modal");

    expect(ym).toHaveBeenNthCalledWith(
      1,
      107194444,
      "reachGoal",
      "card_created",
      { card_type: "fact" },
    );
    expect(ym).toHaveBeenNthCalledWith(
      2,
      107194444,
      "reachGoal",
      "connection_created",
      { connection_type: "relates" },
    );
    expect(ym).toHaveBeenNthCalledWith(
      3,
      107194444,
      "reachGoal",
      "phase_changed",
      { phase: "connections" },
    );
    expect(ym).toHaveBeenNthCalledWith(
      4,
      107194444,
      "reachGoal",
      "special_question_used",
      undefined,
    );
    expect(ym).toHaveBeenNthCalledWith(
      5,
      107194444,
      "reachGoal",
      "session_exported",
      { export_type: "image" },
    );
    expect(ym).toHaveBeenNthCalledWith(
      6,
      107194444,
      "reachGoal",
      "voice_input_used",
      undefined,
    );
    expect(ym).toHaveBeenNthCalledWith(
      7,
      107194444,
      "reachGoal",
      "text_input_used",
      undefined,
    );
    expect(ym).toHaveBeenNthCalledWith(
      8,
      107194444,
      "reachGoal",
      "upgrade_clicked",
      { plan: "monthly", surface: "paywall_modal" },
    );
  });
});
