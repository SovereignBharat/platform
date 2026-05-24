# SovereignBharat Model Registry

Central registry for AI models and runtime artifacts.

## Responsibilities

- Model registration
- Versioning
- Metadata storage
- Deployment tracking
- Artifact references
- Runtime compatibility
- Auditability

## Registry Objects

- Model
- Version
- Artifact
- Runtime
- Deployment
- Evaluation

## Example Metadata

```json
{
  "name": "sb-llm-7b",
  "framework": "transformers",
  "runtime": "vllm",
  "quantization": "fp16"
}
```
