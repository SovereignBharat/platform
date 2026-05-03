# OpenStack Cloud Platform

Enterprise cloud platform powered by OpenStack. Build and scale your infrastructure with compute, storage, and networking.

## Documentation

- [Quick Start Guide](#quick-start)
- [CLI Reference](#cli-reference)
- [API Reference](#api-reference)
- [Security](#security)

---

## Quick Start

### 1. Start the Dashboard

Open `cloud-platform.html` in your browser for the web console.

### 2. Use the Python SDK

```python
from openstack_sdk import OpenStackClient

# Create client (mock mode for testing)
client = OpenStackClient(mock_mode=True)

# Create an instance
instance = client.create_instance(
    name='web-server',
    image_id='img-ubuntu-2204',
    flavor_id='t1.small'
)
print(f"Created: {instance.name} at {instance.ip_address}")
```

### 3. Use the CLI

```bash
# List instances
python3 cloud_cli.py list

# Create instance
python3 cloud_cli.py create my-server --flavor t1.small

# List flavors
python3 cloud_cli.py flavors
```

---

## Available Resources

### Flavors

| Flavor | vCPUs | RAM | Disk |
|--------|-------|-----|------|
| t1.nano | 1 | 512MB | 5GB |
| t1.micro | 1 | 1GB | 10GB |
| t1.small | 2 | 2GB | 20GB |
| t1.medium | 4 | 4GB | 40GB |
| t1.large | 8 | 8GB | 80GB |
| t1.xlarge | 16 | 16GB | 160GB |

### Images
- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS
- CentOS Stream 9
- Debian 12
- Fedora 40
- Rocky Linux 9

---

## CLI Reference

### Instance Commands
```bash
python3 cloud_cli.py list              # List all instances
python3 cloud_cli.py create <name>  # Create instance
python3 cloud_cli.py start --name <instance>   # Start instance
python3 cloud_cli.py stop --name <instance>  # Stop instance
python3 cloud_cli.py delete --name <instance>  # Delete instance
python3 cloud_cli.py reboot --name <instance>    # Reboot instance
```

### Resource Commands
```bash
python3 cloud_cli.py flavors        # List flavors
python3 cloud_cli.py images       # List images
python3 cloud_cli.py volumes    # List volumes
python3 cloud_cli.py networks   # List networks
```

### Info Commands
```bash
python3 cloud_cli.py usage         # Usage statistics
python3 cloud_cli.py billing     # Billing summary
python3 cloud_cli.py console  # Get instance console
```

---

## API Reference

```python
from openstack_sdk import OpenStackClient

client = OpenStackClient(mock_mode=True)

# Compute
instance = client.create_instance(name, image_id, flavor_id)
client.start_instance(instance.id)
client.stop_instance(instance.id)
client.delete_instance(instance.id)

# Storage
volume = client.create_volume(name, size_gb)
client.attach_volume(volume.id, instance.id)

# Networking  
network = client.create_network(name, cidr)
```

---

## Security

- Input validation on all user inputs
- Rate limiting (100 req/min)
- Resource quotas
- Secure token generation
- Password hashing (PBKDF2)
- Audit logging

See [OPENSTACK_CLOUD_PLATFORM.md](OPENSTACK_CLOUD_PLATFORM.md) for full architecture details.

---

*Powered by OpenStack*