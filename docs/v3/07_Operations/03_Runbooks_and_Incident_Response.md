# Runbooks and Incident Response

## Incident framework

| Severity | Example | Response |
|---|---|---|
| SEV-1 | Confirmed cross-user exposure, widespread corruption/unavailability | Immediate incident command, containment, executive/legal/privacy escalation. |
| SEV-2 | Major feature unavailable, projection backlog beyond SLO, limited integrity risk | Urgent owner response and controlled mitigation. |
| SEV-3 | Degraded non-critical workflow or capacity warning | Business-hours remediation with tracking. |

Every incident records commander, timeline, affected versions/data scope, containment, evidence preservation, communications, regulatory assessment, recovery validation and blameless corrective review.

## Required runbooks

| Runbook | First safe actions |
|---|---|
| Auth/verifier outage | Confirm dependency, fail closed, stop risky retries, communicate, restore/validate revocation. |
| Cross-user access suspicion | Disable affected route/gate, preserve audit/logs, revoke relevant sessions/grants, determine exposure before broad statements. |
| Calculation integrity defect | Freeze affected projections, preserve facts/versions, mark outputs unavailable/partial, correct engine and rebuild deterministically. |
| Database failover | Stop unsafe deploys, validate writer/replica/pool, reconcile outbox/checkpoints after recovery. |
| Queue/projection backlog | Identify poison/saturation, apply backpressure/scale, preserve ordering/idempotency, verify freshness. |
| Malicious document | Keep quarantine, disable access, identify scanner/policy scope, rotate/notify only as required. |
| Object/scanner outage | Disable upload/download as applicable, retain pending metadata, never mark unscanned clean. |
| Import poison file | Isolate job/parser version, prevent retries storm, preserve staged evidence safely. |
| Secret/token compromise | Revoke/rotate, invalidate sessions/keys, inspect use, redeploy safely and assess exposure. |
| Failed deployment/migration | Halt rollout, choose app rollback or forward repair, never destructive reset; validate data/traffic. |
| Backup restore | Follow isolated restore, integrity/checksum and application reconciliation; document achieved RPO/RTO. |
| Privacy workflow failure | Stop expiry/deletion claims, preserve request state, retry safely and escalate deadline risk. |

## Communications and learning

User messaging states known impact and action without speculation or sensitive detail. Post-incident actions receive owners/dates and update tests, monitors, runbooks, threat model and architecture decisions.

