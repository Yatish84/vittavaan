# Security, Performance and Recovery Test Plan

## Security acceptance

- Token tampering, algorithm/key/issuer/audience/time/revocation failures.
- IDOR for every person, household, holding, transaction, liability, import, document, goal and audit endpoint.
- Grant escalation, expired/revoked grants, totals-only inference and administrator owner-action attempts.
- CSRF, XSS, injection, mass assignment, pagination/filter abuse and rate-limit bypass.
- Malicious file/type spoof, decompression/resource abuse, CSV formula injection and signed-URL replay.
- Event replay/forgery, idempotency conflicts, concurrency races and audit mutation attempts.
- Log/trace/error leakage inspection and secret scanning.

## Performance workload

Model 100,000 registered users, 10,000 concurrent sessions at target peak, portfolios up to 1,000 active holdings/10,000 events, mixed dashboard/list/detail/write/import/document traffic, projection workers and auth verification. Test cold/warm cache, replica lag, connection pool, queue backpressure and large file boundaries.

Pass criteria are the NFR3 p95/p99/freshness SLOs with no correctness/security degradation. Capacity tests determine autoscaling and partition thresholds; they do not merely report maximum requests per second.

## Resilience experiments

Auth verifier/JWKS outage, Redis unavailable, PostgreSQL failover, queue stopped/backlogged, worker crash mid-job, duplicate/out-of-order events, object/scanner outage, benchmark/notification failure and partial deployment. Verify documented degraded behavior, alerts and recovery.

## Recovery drills

- Restore PostgreSQL to an approved point and reconcile object metadata.
- Restore versioned objects and verify checksums/access controls.
- Rebuild every projection from authoritative facts and compare golden checksums.
- Replay outbox/dead-letter without duplicate effects.
- Recover from failed expand/migrate deployment.
- Demonstrate RPO ≤5 minutes and RTO ≤60 minutes or revise/approve targets.

Production readiness requires recorded evidence, timestamps, artifact versions, deviations, remediation owners and re-test results.

