import { fireEvent, render, screen, waitFor } from "@testing-library/svelte";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import TooltipOverlay from "./TooltipOverlay.svelte";
import { setLocale } from "../stores/i18n";
import { onboarding } from "../stores/onboarding";

describe("TooltipOverlay", () => {
  beforeEach(() => {
    setLocale("en");
    onboarding.reset();
  });

  afterEach(() => {
    onboarding.reset();
    setLocale("en");
  });

  it("keeps the question step active until the first cards appear", async () => {
    render(TooltipOverlay);

    onboarding.sync({
      hasActiveBoard: true,
      cardCount: 0,
      connectionCount: 0,
      phase: "question",
      isDemoBoard: false,
    });

    const startButton = await screen.findByRole("button", { name: "Start" });
    expect(startButton).toBeDisabled();
    expect(
      screen.getByText("Send the first message to continue."),
    ).toBeInTheDocument();

    onboarding.sync({
      hasActiveBoard: true,
      cardCount: 2,
      connectionCount: 0,
      phase: "facts",
      isDemoBoard: false,
    });

    await waitFor(() =>
      expect(screen.getByRole("button", { name: "Start" })).toBeEnabled(),
    );
    expect(
      screen.getByText("Cards are on the board. Continue."),
    ).toBeInTheDocument();

    await fireEvent.click(screen.getByRole("button", { name: "Start" }));
    expect(screen.getByRole("button", { name: "Next" })).toBeDisabled();
  });
});
