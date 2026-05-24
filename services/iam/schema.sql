create table if not exists users (
  id uuid primary key,
  email text unique not null,
  name text,
  password_hash text,
  created_at timestamptz not null default now()
);

create table if not exists roles (
  id uuid primary key,
  name text unique not null,
  description text,
  created_at timestamptz not null default now()
);

create table if not exists permissions (
  id uuid primary key,
  action text not null,
  resource text not null,
  created_at timestamptz not null default now(),
  unique(action, resource)
);

create table if not exists user_roles (
  user_id uuid not null references users(id),
  role_id uuid not null references roles(id),
  primary key(user_id, role_id)
);

create table if not exists role_permissions (
  role_id uuid not null references roles(id),
  permission_id uuid not null references permissions(id),
  primary key(role_id, permission_id)
);

create table if not exists api_keys (
  id uuid primary key,
  user_id uuid not null references users(id),
  name text not null,
  key_hash text not null,
  revoked_at timestamptz,
  created_at timestamptz not null default now()
);
