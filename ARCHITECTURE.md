# SovereignBharat Architecture

## Platform Layers

```txt
Users
  ↓
Console UI
  ↓
API Gateway
  ↓
Control Plane
  ├── IAM
  ├── Cluster Manager
  ├── GPU Scheduler
  ├── AI Runtime
  ├── Workflow Engine
  ├── Observability
  ├── Governance Engine
  └── Deployment Manager
```

## Monorepo Structure

```txt
apps/
services/
packages/
infrastructure/
ai/
agents/
protocols/
.github/
```

## Core Technologies

### Frontend
- Next.js
- TypeScript
- TailwindCSS
- shadcn/ui

### Backend
- Go
- Rust
- Python
- Node.js

### Infrastructure
- Kubernetes
- Helm
- Terraform
- ArgoCD

### AI Stack
- vLLM
- Ray
- PyTorch
- Qdrant
- LangGraph

### Data
- PostgreSQL
- Redis
- ClickHouse
- MinIO
- SurrealDB
