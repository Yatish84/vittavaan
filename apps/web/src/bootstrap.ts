export type PrincipalType = "PERSON" | "SERVICE" | "SUPPORT";
export type PrincipalStatus = "ACTIVE" | "SUSPENDED" | "CLOSED";

export interface BootstrapResponse {
  principal: {
    principal_id: string;
    principal_type: PrincipalType;
    status: PrincipalStatus;
  };
  first_run_required: boolean;
  next_route: string;
  permitted_person_ids: string[];
  permitted_household_ids: string[];
}

export type BootstrapFailureKind = "unauthenticated" | "denied" | "unavailable";

export class BootstrapFailure extends Error {
  constructor(readonly kind: BootstrapFailureKind) {
    super(kind);
    this.name = "BootstrapFailure";
  }
}

export interface BootstrapClient {
  load(accessToken: string, signal: AbortSignal): Promise<BootstrapResponse>;
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === "string");
}

function isBootstrapResponse(value: unknown): value is BootstrapResponse {
  if (typeof value !== "object" || value === null) return false;
  const candidate = value as Record<string, unknown>;
  const principal = candidate.principal;
  if (typeof principal !== "object" || principal === null) return false;
  const identity = principal as Record<string, unknown>;
  return (
    typeof identity.principal_id === "string" &&
    ["PERSON", "SERVICE", "SUPPORT"].includes(String(identity.principal_type)) &&
    ["ACTIVE", "SUSPENDED", "CLOSED"].includes(String(identity.status)) &&
    typeof candidate.first_run_required === "boolean" &&
    typeof candidate.next_route === "string" &&
    isStringArray(candidate.permitted_person_ids) &&
    isStringArray(candidate.permitted_household_ids)
  );
}

export class HttpBootstrapClient implements BootstrapClient {
  constructor(private readonly apiBaseUrl = "/api/v1") {}

  async load(accessToken: string, signal: AbortSignal): Promise<BootstrapResponse> {
    const response = await fetch(`${this.apiBaseUrl}/bootstrap`, {
      method: "GET",
      headers: { Authorization: `Bearer ${accessToken}` },
      cache: "no-store",
      credentials: "omit",
      redirect: "error",
      signal,
    });
    if (response.status === 401) throw new BootstrapFailure("unauthenticated");
    if (response.status === 403) throw new BootstrapFailure("denied");
    if (!response.ok) throw new BootstrapFailure("unavailable");

    let payload: unknown;
    try {
      payload = await response.json();
    } catch {
      throw new BootstrapFailure("unavailable");
    }
    if (!isBootstrapResponse(payload)) throw new BootstrapFailure("unavailable");
    return payload;
  }
}
