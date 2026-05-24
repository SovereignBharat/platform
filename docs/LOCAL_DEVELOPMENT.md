# SovereignBharat Local Development

## Requirements

- Node.js 20+
- pnpm
- Go 1.22+
- Docker
- Kubernetes (optional)

## Install Dependencies

```bash
pnpm install
```

## Run Local Infrastructure

```bash
docker compose -f docker-compose.sovereign.yml up
```

## Run Web App

```bash
cd apps/web
pnpm dev
```

## Run Console

```bash
cd apps/console
pnpm dev
```

## Run Control Plane

```bash
cd services/control-plane
go run .
```

## Run Gateway

```bash
cd services/gateway
go run .
```

## Kubernetes Namespace

```bash
kubectl apply -f infrastructure/kubernetes/namespace.yaml
```
