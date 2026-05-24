# SovereignBharat Workflow Engine

Distributed workflow orchestration for sovereign AI and cloud workloads.

## Responsibilities

- DAG execution
- Retry handling
- Human approval steps
- Event-driven triggers
- Agent workflow orchestration
- Long-running job state
- Failure recovery

## Runtime States

```txt
created -> scheduled -> running -> completed
                         └── failed
                         └── blocked
                         └── cancelled
```

## Future Integrations

- Temporal
- NATS
- Kubernetes Jobs
- Agent runtime
- Governance policy engine
