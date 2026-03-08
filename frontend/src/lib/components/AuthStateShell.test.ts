import { fireEvent, render, screen } from "@testing-library/svelte";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import AuthStateShell from "./AuthStateShell.svelte";
import { setLocale } from "../stores/i18n";

describe("AuthStateShell", () => {
  beforeEach(() => {
    setLocale("en");
  });

  afterEach(() => {
    setLocale("en");
  });

  it("renders the session-expired recovery copy and actions", async () => {
    const onRetry = vi.fn();
    const onRelogin = vi.fn();

    render(AuthStateShell, {
      props: {
        error: "session_expired",
        onRetry,
        onRelogin,
      },
    });

    expect(
      screen.getByRole("heading", { name: "Your session ended" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Your boards are still here. Sign in again to reopen them."),
    ).toBeInTheDocument();

    await fireEvent.click(screen.getByRole("button", { name: "Try again" }));
    await fireEvent.click(screen.getByRole("button", { name: "Sign in again" }));

    expect(onRetry).toHaveBeenCalledOnce();
    expect(onRelogin).toHaveBeenCalledOnce();
  });

  it("renders the transient auth-failure copy", () => {
    render(AuthStateShell, {
      props: {
        error: "auth_failed",
        onRetry: vi.fn(),
        onRelogin: vi.fn(),
      },
    });

    expect(
      screen.getByRole("heading", { name: "Sign-in needs another try" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("We could not confirm your session right now. Retry or open sign-in again."),
    ).toBeInTheDocument();
  });
});
