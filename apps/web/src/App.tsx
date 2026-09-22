import { useEffect, useState } from "react";
import { BootstrapGate } from "./BootstrapGate";
import type { BootstrapClient } from "./bootstrap";
import { HttpBootstrapClient } from "./bootstrap";
import type { HandoffClient } from "./handoff";
import { HttpHandoffClient } from "./handoff";

const bootstrapClient = new HttpBootstrapClient();
const handoffClient = new HttpHandoffClient();

interface VittavaanAppProps {
  bootstrap?: BootstrapClient;
  handoff?: HandoffClient;
}

type EntryState =
  | { kind: "signed-out" }
  | { kind: "working" }
  | { kind: "ready"; accessToken: string }
  | { kind: "unavailable" };

export function VittavaanApp({
  bootstrap = bootstrapClient,
  handoff = handoffClient,
}: VittavaanAppProps) {
  const [entry, setEntry] = useState<EntryState>({ kind: "working" });

  useEffect(() => {
    const parameters = new URLSearchParams(window.location.search);
    const code = parameters.get("code");
    const state = parameters.get("state");
    if (window.location.pathname !== "/auth/return" || !code || !state) {
      void Promise.resolve().then(() => setEntry({ kind: "signed-out" }));
      return;
    }
    window.history.replaceState(null, "", "/");
    handoff.exchange(code, state).then(
      (accessToken) => setEntry({ kind: "ready", accessToken }),
      () => setEntry({ kind: "unavailable" }),
    );
  }, [handoff]);

  async function startSignIn() {
    setEntry({ kind: "working" });
    try {
      const authorizationUrl = await handoff.start();
      window.location.assign(authorizationUrl);
    } catch {
      setEntry({ kind: "unavailable" });
    }
  }

  if (entry.kind === "working") {
    return (
      <main>
        <section className="state-card" aria-labelledby="entry-title" aria-live="polite">
          <p className="eyebrow">Secure access</p>
          <h1 id="entry-title">Connecting securely</h1>
          <p role="status">Preparing your Vittavaan session…</p>
        </section>
      </main>
    );
  }
  if (entry.kind === "unavailable") {
    return (
      <main>
        <section className="state-card" aria-labelledby="entry-title" aria-live="polite">
          <p className="eyebrow">Temporary issue</p>
          <h1 id="entry-title">Secure sign-in could not be completed</h1>
          <p>No access was granted. Please return to sign in and try again.</p>
          <button type="button" onClick={() => void startSignIn()}>
            Return to sign in
          </button>
        </section>
      </main>
    );
  }
  return (
    <BootstrapGate
      accessToken={entry.kind === "ready" ? entry.accessToken : null}
      client={bootstrap}
      onSignInRequested={() => void startSignIn()}
    />
  );
}
