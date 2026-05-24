# SovereignBharat API Gateway

## Responsibilities

- API routing
- Authentication middleware
- Rate limiting
- Request tracing
- Streaming support
- Service discovery
- Reverse proxying

## Public Routes

```txt
/health
/v1/chat/completions
/v1/embeddings
```

## Internal Services

```txt
control-plane
inference-engine
iam
policy-engine
model-registry
workflow-engine
```

## Request Flow

```txt
Client -> Gateway -> Middleware -> Internal Service -> Response
```
