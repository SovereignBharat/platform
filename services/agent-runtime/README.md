# SovereignBharat Agent Runtime

Agent execution layer for sovereign AI workflows.

## Responsibilities

- Agent lifecycle management
- Tool execution
- Memory access controls
- Workflow participation
- Human approval gates
- Runtime policy checks
- Execution audit trails

## Runtime States

```txt
registered -> ready -> executing -> completed
                         └── blocked
                         └── failed
                         └── terminated
```

## Core Objects

- Agent
- Tool
- Memory
- Execution
- Policy
- Approval
- Audit Event
