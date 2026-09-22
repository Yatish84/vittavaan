import { useEffect, useState } from "react";
import type { BootstrapClient, BootstrapResponse } from "./bootstrap";
import { BootstrapFailure } from "./bootstrap";

type ViewState =
  | { kind: "signed-out" }
  | { kind: "loading" }
  | { kind: "first-run"; bootstrap: BootstrapResponse }
  | { kind: "ready"; bootstrap: BootstrapResponse }
  | { kind: "denied" }
  | { kind: "unavailable" };

interface BootstrapGateProps {
  accessToken: string | null;
  client: BootstrapClient;
  onSignInRequested?: () => void;
}

function SignedOut({ onSignInRequested }: { onSignInRequested: (() => void) | undefined }) {
  return (
    <StateCard eyebrow="Secure access" title="Sign in to Vittavaan">
      <p>Your sign-in is handled securely by the separate Vittavaan identity service.</p>
      <button type="button" disabled={!onSignInRequested} onClick={onSignInRequested}>
        Continue to sign in
      </button>
      {!onSignInRequested && (
        <p className="supporting-text">The secure sign-in connection is being configured.</p>
      )}
    </StateCard>
  );
}

function StateCard({
  eyebrow,
  title,
  children,
  live = false,
}: {
  eyebrow: string;
  title: string;
  children: React.ReactNode;
  live?: boolean;
}) {
  return (
    <main>
      <section className="state-card" aria-labelledby="state-title" aria-live={live ? "polite" : "off"}>
        <p className="eyebrow">{eyebrow}</p>
        <h1 id="state-title">{title}</h1>
        {children}
      </section>
    </main>
  );
}

export function BootstrapGate({ accessToken, client, onSignInRequested }: BootstrapGateProps) {
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<ViewState>(
    accessToken ? { kind: "loading" } : { kind: "signed-out" },
  );

  useEffect(() => {
    if (!accessToken) return;
    const controller = new AbortController();
    client.load(accessToken, controller.signal).then(
      (bootstrap) => {
        setState(
          bootstrap.first_run_required
            ? { kind: "first-run", bootstrap }
            : { kind: "ready", bootstrap },
        );
      },
      (error: unknown) => {
        if (controller.signal.aborted) return;
        if (error instanceof BootstrapFailure && error.kind === "unauthenticated") {
          setState({ kind: "signed-out" });
        } else if (error instanceof BootstrapFailure && error.kind === "denied") {
          setState({ kind: "denied" });
        } else {
          setState({ kind: "unavailable" });
        }
      },
    );
    return () => controller.abort();
  }, [accessToken, attempt, client]);

  if (!accessToken) return <SignedOut onSignInRequested={onSignInRequested} />;
  if (state.kind === "signed-out") return <SignedOut onSignInRequested={onSignInRequested} />;
  if (state.kind === "loading") {
    return (
      <StateCard eyebrow="Secure access" title="Opening your portfolio" live>
        <p role="status">Checking your secure Vittavaan profile…</p>
      </StateCard>
    );
  }
  if (state.kind === "denied") {
    return (
      <StateCard eyebrow="Account access" title="Access is unavailable">
        <p>This Vittavaan profile cannot currently be used. Contact your support team for help.</p>
      </StateCard>
    );
  }
  if (state.kind === "unavailable") {
    return (
      <StateCard eyebrow="Temporary issue" title="We could not open your portfolio" live>
        <p>Your information is safe. Please wait a moment and try again.</p>
        <button
          type="button"
          onClick={() => {
            setState({ kind: "loading" });
            setAttempt((value) => value + 1);
          }}
        >
          Try again
        </button>
      </StateCard>
    );
  }
  if (state.kind === "first-run") {
    return (
      <StateCard eyebrow="Welcome to Vittavaan" title="Let’s set up your portfolio">
        <p>Start by telling us about your household. You can add assets and liabilities afterward.</p>
        <a className="button-link" href={state.bootstrap.next_route}>
          Start account setup
        </a>
      </StateCard>
    );
  }
  return (
    <StateCard eyebrow="Portfolio" title="Your portfolio is ready">
      <p>Your secure profile has loaded successfully.</p>
    </StateCard>
  );
}
