import { fireEvent, render, screen } from "@testing-library/svelte";
import { get } from "svelte/store";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import HelpOverlay from "./HelpOverlay.svelte";
import { helpOverlay } from "../stores/help";
import { onboarding } from "../stores/onboarding";
import { setLocale } from "../stores/i18n";

describe("HelpOverlay", () => {
  beforeEach(() => {
    setLocale("en");
    onboarding.reset();
    helpOverlay.close();
  });

  afterEach(() => {
    helpOverlay.close();
    onboarding.reset();
    setLocale("en");
  });

  it("restarts the tutorial from the desktop help popover", async () => {
    onboarding.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 1,
      hasMovedCard: true,
      phase: "connections",
      isDemoBoard: false,
    });
    onboarding.complete();
    helpOverlay.open();

    render(HelpOverlay);

    expect(screen.getByText("Guided tour")).toBeInTheDocument();
    await fireEvent.click(
      screen.getByRole("button", { name: "Restart tutorial" }),
    );

    expect(get(onboarding).completedSteps.size).toBe(0);
    expect(get(onboarding).activeStep).toBe("question");
    expect(screen.queryByRole("button", { name: "Restart tutorial" })).not.toBeInTheDocument();
  });
});
