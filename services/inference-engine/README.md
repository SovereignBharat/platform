# SovereignBharat Inference Engine

AI inference runtime for sovereign model serving.

## Responsibilities

- Model serving
- Chat completions API compatibility
- Embeddings API compatibility
- Streaming responses
- GPU-aware routing
- Model metadata resolution
- Runtime telemetry

## Suggested Runtime Stack

- vLLM
- Ray Serve
- TensorRT-LLM
- Kubernetes
- NVIDIA GPU Operator

## API Surface

```txt
GET  /health
GET  /v1/models
POST /v1/chat/completions
POST /v1/embeddings
```
