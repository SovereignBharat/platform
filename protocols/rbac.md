# SovereignBharat RBAC Protocol

## Core Objects

- User
- Organization
- Workspace
- Role
- Permission
- API Key
- Policy

## Role Hierarchy

```txt
Platform Admin
  ├── Organization Admin
  │     ├── Workspace Admin
  │     │     ├── Developer
  │     │     └── Viewer
```

## Permission Model

Permissions follow:

```txt
resource:action
```

Examples:

```txt
cluster:create
cluster:delete
model:deploy
workflow:execute
agent:run
```
