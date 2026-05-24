# SovereignBharat Issue Plan

## P0 — IAM Authentication

Goal: implement authentication and authorization.

Tasks:
- JWT signing and verification
- OIDC integration
- API key lifecycle
- RBAC middleware
- Auth audit events

## P0 — Control Plane Persistence

Goal: connect control plane APIs to PostgreSQL.

Tasks:
- database connection layer
- repository interfaces
- migrations
- organization/workspace/project APIs
- cluster and deployment APIs

## P0 — Gateway Middleware

Goal: make gateway production-ready.

Tasks:
- request logging
- rate limiting
- auth forwarding
- trace IDs
- reverse proxy routing

## P1 — Inference Runtime

Goal: provide OpenAI-compatible inference APIs.

Tasks:
- model list endpoint
- chat completion endpoint
- embeddings endpoint
- model registry integration
- GPU routing hooks

## P1 — Observability

Goal: add platform-wide telemetry.

Tasks:
- OpenTelemetry middleware
- Prometheus metrics
- structured logs
- trace propagation

## P1 — Console UI

Goal: build the first usable cloud console.

Tasks:
- dashboard
- clusters page
- deployments page
- models page
- agents page
- workflows page
- security page
