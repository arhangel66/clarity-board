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
      phase: "facts",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("cards");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(get(store).activeStep).toBe("connections");
    expect(get(store).canAdvance).toBe(false);

    store.complete();
    expect(get(store).completedSteps.has("connections")).toBe(false);

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 1,
      phase: "facts",
      isDemoBoard: false,
    });
    expect(get(store).activeStep).toBe("connections");
    expect(get(store).canAdvance).toBe(true);

    store.complete();
    expect(get(store).activeStep).toBeNull();

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 1,
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
      phase: "question",
      isDemoBoard: false,
    });
    expect(get(reloadedStore).isTourComplete).toBe(true);
    expect(get(reloadedStore).activeStep).toBeNull();
  });

  it("restart clears stored progress and reactivates the current eligible step", () => {
    const store = createOnboardingStore(localStorage);

    store.sync({
      hasActiveBoard: true,
      cardCount: 3,
      connectionCount: 1,
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
      phase: "facts",
      isDemoBoard: false,
    });

    expect(get(store).isTourComplete).toBe(true);
    expect(get(store).activeStep).toBeNull();
  });
});
