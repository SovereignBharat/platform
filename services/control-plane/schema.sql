create table if not exists organizations (
  id uuid primary key,
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists workspaces (
  id uuid primary key,
  organization_id uuid not null references organizations(id),
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists projects (
  id uuid primary key,
  workspace_id uuid not null references workspaces(id),
  name text not null,
  created_at timestamptz not null default now()
);

create table if not exists clusters (
  id uuid primary key,
  project_id uuid not null references projects(id),
  name text not null,
  region text not null,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);

create table if not exists deployments (
  id uuid primary key,
  project_id uuid not null references projects(id),
  name text not null,
  image text not null,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);

create table if not exists audit_logs (
  id uuid primary key,
  organization_id uuid references organizations(id),
  actor text not null,
  action text not null,
  resource text not null,
  created_at timestamptz not null default now()
);
