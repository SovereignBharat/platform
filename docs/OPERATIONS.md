# SovereignBharat Operations Guide

## Core Operational Domains

### Infrastructure
- Kubernetes cluster health
- Node availability
- GPU utilization
- Network health
- Storage availability

### Runtime
- Workflow execution
- Agent runtime state
- Deployment reconciliation
- Event bus throughput
- API latency

### Governance
- Audit log integrity
- Policy enforcement
- IAM events
- Approval workflows
- Tenant isolation

## Monitoring Stack

- Prometheus
- Grafana
- Loki
- Tempo
- OpenTelemetry

## Operational Metrics

```txt
api.requests
runtime.failures
gpu.utilization
workflow.duration
deployment.status
policy.denials
```

## Incident Response

1. Identify failing subsystem
2. Check audit logs
3. Validate runtime events
4. Verify Kubernetes health
5. Roll back failed deployments if needed
