import { fireEvent, render, screen } from "@testing-library/svelte";
import { get } from "svelte/store";
import { afterEach, beforeEach, describe, expect, it } from "vitest";

import MobileDrawer from "./MobileDrawer.svelte";
import { boards } from "../stores/boards";
import { cards } from "../stores/cards";
import { openDrawer, closeDrawer } from "../stores/drawer";
import { onboarding } from "../stores/onboarding";
import { setLocale } from "../stores/i18n";

describe("MobileDrawer", () => {
  beforeEach(() => {
    setLocale("en");
    boards.reset();
    cards.clear();
    onboarding.reset();
    closeDrawer();
  });

  afterEach(() => {
    closeDrawer();
    onboarding.reset();
    cards.clear();
    boards.reset();
    setLocale("en");
  });

  it("exposes tutorial restart inside the mobile drawer", async () => {
    onboarding.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 1,
      phase: "connections",
      isDemoBoard: false,
    });
    onboarding.complete();
    openDrawer();

    render(MobileDrawer);

    expect(screen.getByText("Guided tour")).toBeInTheDocument();
    await fireEvent.click(
      screen.getByRole("button", { name: "Restart tutorial" }),
    );

    expect(get(onboarding).completedSteps.size).toBe(0);
    expect(get(onboarding).activeStep).toBe("question");
  });
});
