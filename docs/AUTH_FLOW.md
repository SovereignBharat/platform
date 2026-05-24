# SovereignBharat Authentication Flow

## Token Issuance

Request:

```http
POST /v1/auth/token
Content-Type: application/json
```

Example body:

```json
{
  "subject": "developer@sovereignbharat.ai",
  "roles": ["developer"]
}
```

Response:

```json
{
  "token": "<jwt-token>"
}
```

## Token Verification

```http
GET /v1/auth/verify
Authorization: Bearer <jwt-token>
```

## Gateway Flow

```txt
Client -> Gateway -> Auth Middleware -> IAM Verification -> Internal Service
```

## Future Enhancements

- OIDC providers
- Refresh tokens
- API key rotation
- Tenant-aware claims
- Service-to-service auth
