import { cleanup, fireEvent, render, screen, within } from "@testing-library/svelte";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import LandingPage from "./LandingPage.svelte";
import { auth } from "../stores/auth";
import { setLocale } from "../stores/i18n";

describe("LandingPage", () => {
  beforeEach(() => {
    setLocale("en");
    delete window.ym;
    vi.restoreAllMocks();

    // Mock IntersectionObserver for scroll-reveal
    globalThis.IntersectionObserver = class {
      observe = vi.fn();
      unobserve = vi.fn();
      disconnect = vi.fn();
      constructor() {}
    } as any;
  });

  afterEach(() => {
    cleanup();
    setLocale("en");
    delete window.ym;
    vi.restoreAllMocks();
  });

  it("keeps pricing CTA clicks in the preview flow until the user explicitly starts free access", async () => {
    const ym = vi.fn();
    const loginSpy = vi.spyOn(auth, "loginWithGoogle").mockResolvedValue();
    window.ym = ym;

    render(LandingPage);

    const monthlyCard = screen.getByText("Unlimited").closest("article");
    expect(monthlyCard).not.toBeNull();

    await fireEvent.click(
      within(monthlyCard as HTMLElement).getByRole("button", { name: "Start free" }),
    );

    expect(loginSpy).not.toHaveBeenCalled();
    expect(ym).toHaveBeenCalledWith(107194444, "reachGoal", "upgrade_clicked", {
      plan: "monthly",
      surface: "landing_pricing",
    });
    expect(screen.getByText(/Unlimited looks like the best fit/i)).toBeInTheDocument();
    expect(screen.getByText(/nothing is charged here/i)).toBeInTheDocument();

    await fireEvent.click(screen.getByRole("button", { name: /continue with free access/i }));

    expect(loginSpy).toHaveBeenCalledOnce();
  });
});
