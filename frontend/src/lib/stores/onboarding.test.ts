import { get } from "svelte/store";
import { beforeEach, describe, expect, it } from "vitest";

import {
  LEGACY_ONBOARDING_STORAGE_KEY,
  LEGACY_TIPS_STORAGE_KEY,
  ONBOARDING_STORAGE_KEY,
  createOnboardingStore,
} from "./onboarding";

describe("onboarding store", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("progresses through eligible steps and persists completion", () => {
    const store = createOnboardingStore(localStorage);

    store.sync({
      hasActiveBoard: true,
      cardCount: 0,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "question",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("question");
    expect(get(store).canAdvance).toBe(false);

    store.complete();
    expect(get(store).completedSteps.size).toBe(0);

    store.sync({
      hasActiveBoard: true,
      cardCount: 2,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "facts",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("question");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(JSON.parse(localStorage.getItem(ONBOARDING_STORAGE_KEY) ?? "{}"))
      .toEqual({
        completedSteps: ["question"],
        isTourComplete: false,
      });

    expect(get(store).activeStep).toBe("cards");
    expect(get(store).canAdvance).toBe(false);

    store.complete();
    expect(get(store).completedSteps.has("cards")).toBe(false);

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "facts",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("cards");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(get(store).activeStep).toBe("move_card");
    expect(get(store).canAdvance).toBe(false);

    store.complete();
    expect(get(store).completedSteps.has("move_card")).toBe(false);

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 0,
      hasMovedCard: true,
      phase: "facts",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("move_card");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(get(store).activeStep).toBeNull();

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 0,
      hasMovedCard: true,
      phase: "gaps",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("blind_spots");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(get(store).isTourComplete).toBe(true);
    expect(get(store).activeStep).toBeNull();

    const reloadedStore = createOnboardingStore(localStorage);
    reloadedStore.sync({
      hasActiveBoard: true,
      cardCount: 0,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "question",
      isDemoBoard: false,
    });
    expect(get(reloadedStore).isTourComplete).toBe(true);
    expect(get(reloadedStore).activeStep).toBeNull();
  });

  it("skipTour skips only the active step", () => {
    const store = createOnboardingStore(localStorage);

    store.sync({
      hasActiveBoard: true,
      cardCount: 0,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "question",
      isDemoBoard: false,
    });

    store.skipTour();
    expect(get(store).isTourComplete).toBe(false);
    expect(get(store).completedSteps).toEqual(new Set(["question"]));
    expect(JSON.parse(localStorage.getItem(ONBOARDING_STORAGE_KEY) ?? "{}")).toEqual({
      completedSteps: ["question"],
      isTourComplete: false,
    });

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "facts",
      isDemoBoard: false,
    });

    expect(get(store).activeStep).toBe("cards");
  });

  it("restart clears stored progress and reactivates the current eligible step", () => {
    const store = createOnboardingStore(localStorage);

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 1,
      hasMovedCard: true,
      phase: "connections",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("question");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(get(store).activeStep).toBe("cards");

    store.restart();
    expect(get(store).completedSteps.size).toBe(0);
    expect(get(store).activeStep).toBe("question");
    expect(get(store).canAdvance).toBe(true);
    expect(JSON.parse(localStorage.getItem(ONBOARDING_STORAGE_KEY) ?? "{}"))
      .toEqual({
        completedSteps: [],
        isTourComplete: false,
      });
  });

  it("keeps legacy onboarding users out of the new tour", () => {
    localStorage.setItem(LEGACY_ONBOARDING_STORAGE_KEY, "true");
    const store = createOnboardingStore(localStorage);

    store.sync({
      hasActiveBoard: true,
      cardCount: 0,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "question",
      isDemoBoard: false,
    });

    expect(get(store).isTourComplete).toBe(true);
    expect(get(store).activeStep).toBeNull();
  });

  it("treats fully seen legacy tips as a completed onboarding tour", () => {
    localStorage.setItem(
      LEGACY_TIPS_STORAGE_KEY,
      JSON.stringify(["inputbar", "cards_added", "connections_hint"]),
    );
    const store = createOnboardingStore(localStorage);

    store.sync({
      hasActiveBoard: true,
      cardCount: 2,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "facts",
      isDemoBoard: false,
    });

    expect(get(store).isTourComplete).toBe(true);
    expect(get(store).activeStep).toBeNull();
  });

  it("migrates an unfinished legacy connections step to move_card", () => {
    localStorage.setItem(
      ONBOARDING_STORAGE_KEY,
      JSON.stringify({
        completedSteps: ["question", "cards", "connections"],
        isTourComplete: false,
      }),
    );

    const store = createOnboardingStore(localStorage);
    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 0,
      hasMovedCard: false,
      phase: "facts",
      isDemoBoard: false,
    });

    expect(get(store).completedSteps.has("move_card")).toBe(true);
    expect(get(store).activeStep).toBeNull();
  });
});
