#!/usr/bin/env python3
"""
OpenStack Cloud Platform - Core Services SDK
This module provides Python interfaces for interacting with OpenStack services.

Supported Services:
- Compute (Nova) - Virtual machine management
- Image (Glance) - Disk images
- Block Storage (Cinder) - Persistent volumes
- Object Storage (Swift) - Object storage
- Network (Neutron) - Networking
- Identity (Keystone) - Authentication
- Orchestration (Heat) - Infrastructure as Code
"""

import os
import json
import time
import hashlib
import uuid
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('OpenStackSDK')


class InstanceState(Enum):
    """Instance states similar to OpenStack Nova"""
    ACTIVE = "active"
    SHUTOFF = "shutoff"
    PAUSED = "paused"
    SUSPENDED = "suspended"
    BUILDING = "building"
    RESIZE = "resize"
    REBOOT = "rebooting"
    ERROR = "error"


class VolumeState(Enum):
    """Volume states similar to OpenStack Cinder"""
    AVAILABLE = "available"
    IN_USE = "in-use"
    CREATING = "creating"
    DELETING = "deleting"
    ERROR = "error"


class NetworkState(Enum):
    """Network states similar to OpenStack Neutron"""
    ACTIVE = "active"
    DOWN = "down"
    BUILDING = "building"
    ERROR = "error"


@dataclass
class Flavor:
    """Compute flavor (hardware profile)"""
    id: str
    name: str
    vcpus: int
    ram_mb: int
    disk_gb: int
    ephemeral_gb: int = 0
    swap_mb: int = 0
    rxtx_factor: float = 1.0
    is_public: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'vcpus': self.vcpus,
            'ram_mb': self.ram_mb,
            'disk_gb': self.disk_gb,
            'ephemeral_gb': self.ephemeral_gb,
            'swap_mb': self.swap_mb,
            'rxtx_factor': self.rxtx_factor,
            'is_public': self.is_public
        }


@dataclass
class Image:
    """Virtual machine image"""
    id: str
    name: str
    status: str = "active"
    min_disk_gb: int = 10
    min_ram_mb: int = 512
    size_bytes: int = 0
    container_format: str = "bare"
    disk_format: str = "qcow2"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'min_disk_gb': self.min_disk_gb,
            'min_ram_mb': self.min_ram_mb,
            'size_bytes': self.size_bytes,
            'container_format': self.container_format,
            'disk_format': self.disk_format,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': self.tags
        }


@dataclass
class Instance:
    """Virtual compute instance"""
    id: str
    name: str
    image_id: str
    flavor_id: str
    status: InstanceState = InstanceState.BUILDING
    ip_address: Optional[str] = None
    floating_ip: Optional[str] = None
    key_name: Optional[str] = None
    security_groups: List[str] = field(default_factory=lambda: ["default"])
    networks: List[str] = field(default_factory=lambda: ["provider"])
    user_data: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'image_id': self.image_id,
            'flavor_id': self.flavor_id,
            'status': self.status.value,
            'ip_address': self.ip_address,
            'floating_ip': self.floating_ip,
            'key_name': self.key_name,
            'security_groups': self.security_groups,
            'networks': self.networks,
            'user_data': self.user_data,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class Volume:
    """Block storage volume"""
    id: str
    name: str
    size_gb: int
    volume_type: str = "SSD"
    status: VolumeState = VolumeState.CREATING
    source_volid: Optional[str] = None
    snapshot_id: Optional[str] = None
    image_id: Optional[str] = None
    attachments: List[Dict[str, str]] = field(default_factory=list)
    encrypted: bool = False
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'size_gb': self.size_gb,
            'volume_type': self.volume_type,
            'status': self.status.value,
            'source_volid': self.source_volid,
            'snapshot_id': self.snapshot_id,
            'image_id': self.image_id,
            'attachments': self.attachments,
            'encrypted': self.encrypted,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class Network:
    """Virtual network"""
    id: str
    name: str
    cidr: str
    state: NetworkState = NetworkState.ACTIVE
    network_type: str = "vxlan"
    segmentation_id: Optional[int] = None
    provider_physical_network: Optional[str] = None
    is_shared: bool = False
    is_external: bool = False
    subnets: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'cidr': self.cidr,
            'state': self.state.value,
            'network_type': self.network_type,
            'segmentation_id': self.segmentation_id,
            'provider_physical_network': self.provider_physical_network,
            'is_shared': self.is_shared,
            'is_external': self.is_external,
            'subnets': self.subnets,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class Subnet:
    """Network subnet"""
    id: str
    name: str
    network_id: str
    cidr: str
    gateway_ip: Optional[str] = None
    dhcp_enabled: bool = True
    allocation_pools: List[Dict[str, str]] = field(default_factory=list)
    dns_nameservers: List[str] = field(default_factory=lambda: ["8.8.8.8", "8.8.4.4"])
    ip_version: int = 4
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'network_id': self.network_id,
            'cidr': self.cidr,
            'gateway_ip': self.gateway_ip,
            'dhcp_enabled': self.dhcp_enabled,
            'allocation_pools': self.allocation_pools,
            'dns_nameservers': self.dns_nameservers,
            'ip_version': self.ip_version
        }


class OpenStackClient:
    """
    Main client for interacting with OpenStack services.
    Provides both mock and real API implementations.
    """
    
    # Default flavors
    DEFAULT_FLAVORS = [
        Flavor("t1.nano", "t1.nano", 1, 512, 5),
        Flavor("t1.micro", "t1.micro", 1, 1024, 10),
        Flavor("t1.small", "t1.small", 2, 2048, 20),
        Flavor("t1.medium", "t1.medium", 4, 4096, 40),
        Flavor("t1.large", "t1.large", 8, 8192, 80),
        Flavor("t1.xlarge", "t1.xlarge", 16, 16384, 160),
    ]
    
    # Default images
    DEFAULT_IMAGES = [
        Image("img-ubuntu-2204", "Ubuntu 22.04 LTS", size_bytes=2_500_000_000),
        Image("img-ubuntu-2404", "Ubuntu 24.04 LTS", size_bytes=3_500_000_000),
        Image("img-centos-9", "CentOS Stream 9", size_bytes=2_000_000_000),
        Image("img-debian-12", "Debian 12", size_bytes=1_500_000_000),
        Image("img-fedora-40", "Fedora 40", size_bytes=2_500_000_000),
        Image("img-rocky-9", "Rocky Linux 9", size_bytes=2_200_000_000),
    ]
    
    def __init__(self, auth_url: str = None, username: str = None, password: str = None,
                 project_name: str = None, domain_name: str = "Default",
                 mock_mode: bool = True):
        """
        Initialize OpenStack client.
        
        Args:
            auth_url: Keystone auth URL
            username: Username for authentication
            password: Password for authentication
            project_name: Project/tenant name
            domain_name: Domain name
            mock_mode: Use mock data instead of real API calls
        """
        self.auth_url = auth_url or os.environ.get('OS_AUTH_URL')
        self.username = username or os.environ.get('OS_USERNAME')
        self.password = password or os.environ.get('OS_PASSWORD')
        self.project_name = project_name or os.environ.get('OS_PROJECT_NAME')
        self.domain_name = domain_name
        self.mock_mode = mock_mode
        
        # Token for API authentication
        self.token = None
        self.token_expires = None
        
        # In-memory data stores (for mock mode)
        self._flavors = {f.id: f for f in self.DEFAULT_FLAVORS}
        self._images = {i.id: i for i in self.DEFAULT_IMAGES}
        self._instances = {}
        self._volumes = {}
        self._networks = {}
        self._subnets = {}
        
        logger.info(f"OpenStack client initialized (mock_mode={mock_mode})")
    
    # ==================== Authentication ====================
    
    def authenticate(self) -> bool:
        """
        Authenticate with Keystone and obtain a token.
        
        Returns:
            True if authentication successful
        """
        if self.mock_mode:
            self.token = f"mock_token_{uuid.uuid4().hex[:16]}"
            logger.info("Mock authentication successful")
            return True
        
        # Real authentication would use Keystone API
        # For now, just log the attempt
        logger.info(f"Authenticating with {self.auth_url}")
        return True
    
    def get_token(self) -> Optional[str]:
        """Get authentication token"""
        return self.token
    
    # ==================== Compute (Nova) ====================
    
    def list_flavors(self) -> List[Flavor]:
        """List available flavors"""
        if self.mock_mode:
            return list(self._flavors.values())
        
        # Real API call would go here
        return list(self._flavors.values())
    
    def get_flavor(self, flavor_id: str) -> Optional[Flavor]:
        """Get flavor by ID"""
        return self._flavors.get(flavor_id)
    
    def create_flavor(self, flavor: Flavor) -> Flavor:
        """Create a new flavor"""
        if self.mock_mode:
            self._flavors[flavor.id] = flavor
            logger.info(f"Created flavor: {flavor.name}")
            return flavor
        
        raise NotImplementedError("Real API flavor creation not implemented")
    
    def delete_flavor(self, flavor_id: str) -> bool:
        """Delete a flavor"""
        if self.mock_mode:
            if flavor_id in self._flavors:
                del self._flavors[flavor_id]
                logger.info(f"Deleted flavor: {flavor_id}")
                return True
            return False
        
        raise NotImplementedError("Real API flavor deletion not implemented")
    
    def list_images(self) -> List[Image]:
        """List available images"""
        if self.mock_mode:
            return list(self._images.values())
        return []
    
    def get_image(self, image_id: str) -> Optional[Image]:
        """Get image by ID"""
        return self._images.get(image_id)
    
    def create_image(self, image: Image) -> Image:
        """Create/register a new image"""
        if self.mock_mode:
            image.id = image.id or f"img-{uuid.uuid4().hex[:8]}"
            image.created_at = datetime.now()
            self._images[image.id] = image
            logger.info(f"Created image: {image.name}")
            return image
        
        raise NotImplementedError("Real API image creation not implemented")
    
    def delete_image(self, image_id: str) -> bool:
        """Delete an image"""
        if self.mock_mode:
            if image_id in self._images:
                del self._images[image_id]
                logger.info(f"Deleted image: {image_id}")
                return True
            return False
        
        raise NotImplementedError("Real API image deletion not implemented")
    
    def list_instances(self) -> List[Instance]:
        """List all instances"""
        if self.mock_mode:
            return list(self._instances.values())
        return []
    
    def get_instance(self, instance_id: str) -> Optional[Instance]:
        """Get instance by ID"""
        return self._instances.get(instance_id)
    
    def create_instance(self, name: str, image_id: str, flavor_id: str,
                      network_ids: List[str] = None, key_name: str = None,
                      security_groups: List[str] = None,
                      user_data: str = None, metadata: Dict[str, str] = None) -> Instance:
        """
        Create (launch) a new instance.
        
        Args:
            name: Instance name
            image_id: Image ID to boot from
            flavor_id: Flavor ID for hardware
            network_ids: Network IDs to attach
            key_name: Key pair name
            security_groups: Security group names
            user_data: User data script (cloud-init)
            metadata: Instance metadata
            
        Returns:
            Created Instance object
        """
        if self.mock_mode:
            instance = Instance(
                id=f"inst-{uuid.uuid4().hex[:8]}",
                name=name,
                image_id=image_id,
                flavor_id=flavor_id,
                status=InstanceState.BUILDING,
                ip_address=None,
                key_name=key_name,
                security_groups=security_groups or ["default"],
                networks=network_ids or ["provider"],
                user_data=user_data,
                metadata=metadata or {},
                created_at=datetime.now()
            )
            
            self._instances[instance.id] = instance
            logger.info(f"Creating instance: {name}")
            
            # Simulate instance creation
            instance.status = InstanceState.ACTIVE
            instance.ip_address = f"10.0.1.{len(self._instances) + 10}"
            
            return instance
        
        raise NotImplementedError("Real API instance creation not implemented")
    
    def start_instance(self, instance_id: str) -> Instance:
        """Start a stopped instance"""
        instance = self._instances.get(instance_id)
        if instance:
            instance.status = InstanceState.ACTIVE
            logger.info(f"Started instance: {instance_id}")
            return instance
        return None
    
    def stop_instance(self, instance_id: str) -> Instance:
        """Stop a running instance"""
        instance = self._instances.get(instance_id)
        if instance:
            instance.status = InstanceState.SHUTOFF
            logger.info(f"Stopped instance: {instance_id}")
            return instance
        return None
    
    def reboot_instance(self, instance_id: str, reboot_type: str = "SOFT") -> Instance:
        """Reboot an instance"""
        instance = self._instances.get(instance_id)
        if instance:
            if instance.status == InstanceState.ACTIVE:
                instance.status = InstanceState.REBOOT
                logger.info(f"Rebooting instance: {instance_id}")
                time.sleep(0.5)  # Simulate reboot time
                instance.status = InstanceState.ACTIVE
            return instance
        return None
    
    def delete_instance(self, instance_id: str) -> bool:
        """Delete an instance"""
        if self.mock_mode:
            if instance_id in self._instances:
                del self._instances[instance_id]
                logger.info(f"Deleted instance: {instance_id}")
                return True
            return False
        return False
    
    def resize_instance(self, instance_id: str, flavor_id: str) -> Instance:
        """Resize an instance (change flavor)"""
        instance = self._instances.get(instance_id)
        if instance:
            instance.status = InstanceState.RESIZE
            logger.info(f"Resizing instance {instance_id} to flavor {flavor_id}")
            time.sleep(1)  # Simulate resize time
            instance.flavor_id = flavor_id
            instance.status = InstanceState.ACTIVE
            return instance
        return None
    
    def get_instance_console(self, instance_id: str) -> Dict[str, str]:
        """Get instance console URL"""
        return {
            'type': 'vnc',
            'url': f"http://console.example.com/vnc/{instance_id}"
        }
    
    def get_instance_vnc(self, instance_id: str) -> str:
        """Get VNC console URL"""
        return f"http://console.example.com/vnc/{instance_id}"
    
    # ==================== Block Storage (Cinder) ====================
    
    def list_volumes(self) -> List[Volume]:
        """List all volumes"""
        if self.mock_mode:
            return list(self._volumes.values())
        return []
    
    def get_volume(self, volume_id: str) -> Optional[Volume]:
        """Get volume by ID"""
        return self._volumes.get(volume_id)
    
    def create_volume(self, name: str, size_gb: int, volume_type: str = "SSD",
                    source_snapshot_id: str = None, image_id: str = None) -> Volume:
        """
        Create a new volume.
        
        Args:
            name: Volume name
            size_gb: Size in GB
            volume_type: Volume type (SSD, HDD, Encrypted)
            source_snapshot_id: Source snapshot ID
            image_id: Source image ID (for bootable volumes)
            
        Returns:
            Created Volume object
        """
        if self.mock_mode:
            volume = Volume(
                id=f"vol-{uuid.uuid4().hex[:8]}",
                name=name,
                size_gb=size_gb,
                volume_type=volume_type,
                status=VolumeState.CREATING,
                snapshot_id=source_snapshot_id,
                image_id=image_id,
                created_at=datetime.now()
            )
            
            self._volumes[volume.id] = volume
            logger.info(f"Creating volume: {name}")
            
            # Simulate volume creation
            volume.status = VolumeState.AVAILABLE
            
            return volume
        
        raise NotImplementedError("Real API volume creation not implemented")
    
    def attach_volume(self, volume_id: str, instance_id: str, device: str = None) -> Volume:
        """Attach volume to instance"""
        volume = self._volumes.get(volume_id)
        if volume:
            attachment = {
                'instance_id': instance_id,
                'device': device or f"/dev/vd{chr(98 + len(volume.attachments))}"
            }
            volume.attachments.append(attachment)
            volume.status = VolumeState.IN_USE
            logger.info(f"Attached volume {volume_id} to {instance_id}")
            return volume
        return None
    
    def detach_volume(self, volume_id: str) -> Volume:
        """Detach volume from instance"""
        volume = self._volumes.get(volume_id)
        if volume:
            volume.attachments = []
            volume.status = VolumeState.AVAILABLE
            logger.info(f"Detached volume {volume_id}")
            return volume
        return None
    
    def extend_volume(self, volume_id: str, new_size_gb: int) -> Volume:
        """Extend volume size"""
        volume = self._volumes.get(volume_id)
        if volume:
            volume.size_gb = new_size_gb
            logger.info(f"Extended volume {volume_id} to {new_size_gb}GB")
            return volume
        return None
    
    def delete_volume(self, volume_id: str) -> bool:
        """Delete a volume"""
        if self.mock_mode:
            if volume_id in self._volumes:
                del self._volumes[volume_id]
                logger.info(f"Deleted volume: {volume_id}")
                return True
            return False
        return False
    
    def create_snapshot(self, volume_id: str, name: str) -> Dict[str, Any]:
        """Create volume snapshot"""
        return {
            'id': f"snap-{uuid.uuid4().hex[:8]}",
            'name': name,
            'volume_id': volume_id,
            'status': 'available',
            'size': self._volumes.get(volume_id).size_gb if volume_id in self._volumes else 0
        }
    
    # ==================== Networking (Neutron) ====================
    
    def list_networks(self) -> List[Network]:
        """List all networks"""
        if self.mock_mode:
            return list(self._networks.values())
        
        # Default networks
        return [
            Network("net-provider", "provider", "192.168.1.0/24",
                   is_external=True, network_type="flat"),
            Network("net-internal", "internal", "10.0.1.0/24",
                   network_type="vxlan"),
        ]
    
    def get_network(self, network_id: str) -> Optional[Network]:
        """Get network by ID"""
        return self._networks.get(network_id)
    
    def create_network(self, name: str, cidr: str, network_type: str = "vxlan",
                   is_shared: bool = False, is_external: bool = False) -> Network:
        """
        Create a new network.
        
        Args:
            name: Network name
            cidr: Network CIDR (e.g., "10.0.2.0/24")
            network_type: Network type (flat, vlan, vxlan, gre)
            is_shared: Allow sharing with other projects
            is_external: Use for external connectivity
            
        Returns:
            Created Network object
        """
        if self.mock_mode:
            network = Network(
                id=f"net-{uuid.uuid4().hex[:8]}",
                name=name,
                cidr=cidr,
                network_type=network_type,
                is_shared=is_shared,
                is_external=is_external,
                state=NetworkState.ACTIVE,
                created_at=datetime.now()
            )
            
            self._networks[network.id] = network
            logger.info(f"Created network: {name}")
            
            return network
        
        raise NotImplementedError("Real API network creation not implemented")
    
    def delete_network(self, network_id: str) -> bool:
        """Delete a network"""
        if self.mock_mode:
            if network_id in self._networks:
                del self._networks[network_id]
                logger.info(f"Deleted network: {network_id}")
                return True
            return False
        return False
    
    def list_subnets(self) -> List[Subnet]:
        """List all subnets"""
        return list(self._subnets.values())
    
    def create_subnet(self, network_id: str, name: str, cidr: str,
                   gateway_ip: str = None, dhcp_enabled: bool = True) -> Subnet:
        """Create a subnet"""
        if self.mock_mode:
            subnet = Subnet(
                id=f"subnet-{uuid.uuid4().hex[:8]}",
                name=name,
                network_id=network_id,
                cidr=cidr,
                gateway_ip=gateway_ip,
                dhcp_enabled=dhcp_enabled
            )
            
            self._subnets[subnet.id] = subnet
            logger.info(f"Created subnet: {name}")
            
            return subnet
        
        raise NotImplementedError("Real API subnet creation not implemented")
    
    def create_router(self, name: str, external_network_id: str = None) -> Dict[str, Any]:
        """Create a router"""
        return {
            'id': f"router-{uuid.uuid4().hex[:8]}",
            'name': name,
            'status': 'active',
            'external_gateway': external_network_id,
            'interfaces': []
        }
    
    def add_interface_router(self, router_id: str, subnet_id: str) -> Dict[str, Any]:
        """Add interface to router"""
        return {
            'router_id': router_id,
            'subnet_id': subnet_id,
            'port_id': f"port-{uuid.uuid4().hex[:8]}"
        }
    
    def create_floating_ip(self, external_network_id: str) -> Dict[str, Any]:
        """Allocate floating IP"""
        return {
            'id': f"fip-{uuid.uuid4().hex[:8]}",
            'floating_ip': f"192.168.1.{100 + len([k for k in self._instances if k.startswith('fip')])}",
            'fixed_ip': None,
            'status': 'ACTIVE',
            'network_id': external_network_id
        }
    
    def associate_floating_ip(self, floating_ip_id: str, instance_id: str) -> Dict[str, Any]:
        """Associate floating IP with instance"""
        instance = self._instances.get(instance_id)
        if instance:
            instance.floating_ip = f"192.168.1.{100 + len(self._instances)}"
            return {'floating_ip': instance.floating_ip}
        return None
    
    def create_security_group(self, name: str, description: str = None) -> Dict[str, Any]:
        """Create security group"""
        return {
            'id': f"sg-{uuid.uuid4().hex[:8]}",
            'name': name,
            'description': description or name,
            'rules': [
                {'direction': 'ingress', 'ethertype': 'IPv4', 'security_group_id': name}
            ]
        }
    
    def create_security_group_rule(self, security_group_id: str,
                                direction: str = "ingress",
                                protocol: str = "tcp",
                                port_range_min: int = None,
                                port_range_max: int = None,
                                remote_ip_prefix: str = None) -> Dict[str, Any]:
        """Create security group rule"""
        return {
            'id': f"rule-{uuid.uuid4().hex[:8]}",
            'security_group_id': security_group_id,
            'direction': direction,
            'protocol': protocol,
            'port_range_min': port_range_min,
            'port_range_max': port_range_max,
            'remote_ip_prefix': remote_ip_prefix
        }
    
    def create_keypair(self, name: str, key_type: str = "ssh") -> Dict[str, Any]:
        """Create key pair"""
        return {
            'id': f"keypair-{uuid.uuid4().hex[:8]}",
            'name': name,
            'type': key_type,
            'public_key': f"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC... {name}"
        }
    
    def delete_keypair(self, name: str) -> bool:
        """Delete key pair"""
        logger.info(f"Deleted key pair: {name}")
        return True
    
    # ==================== Usage & Billing ====================
    
    def get_usage(self, tenant_id: str = None, start: datetime = None,
                 end: datetime = None) -> Dict[str, Any]:
        """Get usage statistics"""
        if self.mock_mode:
            return {
                'tenant_id': tenant_id or 'mock-tenant',
                'start': start.isoformat() if start else datetime.now().isoformat(),
                'end': end.isoformat() if end else datetime.now().isoformat(),
                'Instances': len(self._instances),
                'vCPUs': sum(f.vcpus for f in [
                    self._flavors[i.flavor_id] for i in self._instances.values()
                ]),
                'RAM': sum(f.ram_mb for f in [
                    self._flavors[i.flavor_id] for i in self._instances.values()
                ]),
                'Disk': sum(f.disk_gb for f in [
                    self._flavors[i.flavor_id] for i in self._instances.values()
                ]),
            }
        return {}
    
    def get_billing_summary(self, tenant_id: str = None) -> Dict[str, Any]:
        """Get billing summary"""
        usage = self.get_usage(tenant_id)
        
        # Calculate costs (example pricing)
        hourly_rates = {
            't1.nano': 0.01,
            't1.micro': 0.02,
            't1.small': 0.05,
            't1.medium': 0.10,
            't1.large': 0.20,
            't1.xlarge': 0.40,
        }
        
        total_cost = 0
        for instance in self._instances.values():
            rate = hourly_rates.get(instance.flavor_id, 0.05)
            total_cost += rate * 24 * 30  # Monthly estimate
        
        return {
            'compute': total_cost,
            'storage': len(self._volumes) * 10,  # $10/GB/month estimate
            'network': 50,  # Base network cost
            'total': total_cost + len(self._volumes) * 10 + 50
        }
    
    # ==================== Utilities ====================
    
    def wait_for_status(self, resource_id: str, target_status: str,
                        check_fn, timeout: int = 300,
                        interval: int = 5) -> bool:
        """
        Wait for a resource to reach a specific status.
        
        Args:
            resource_id: Resource ID to check
            target_status: Desired status
            check_fn: Function to check current status
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds
            
        Returns:
            True if target status reached, False if timeout
        """
        elapsed = 0
        while elapsed < timeout:
            status = check_fn(resource_id)
            if status == target_status:
                return True
            time.sleep(interval)
            elapsed += interval
        return False
    
    def to_json(self, obj: Any) -> str:
        """Convert object to JSON string"""
        if hasattr(obj, 'to_dict'):
            return json.dumps(obj.to_dict(), indent=2)
        return json.dumps(obj, indent=2)


# Convenience functions
def create_client(**kwargs) -> OpenStackClient:
    """Create a new OpenStack client"""
    return OpenStackClient(**kwargs)


# Example usage
if __name__ == "__main__":
    # Create client in mock mode
    client = OpenStackClient(mock_mode=True)
    
    print("=" * 50)
    print("OpenStack Cloud Platform SDK - Demo")
    print("=" * 50)
    
    # List flavors
    print("\n📦 Available Flavors:")
    for flavor in client.list_flavors():
        print(f"  {flavor.name}: {flavor.vcpus} vCPU, {flavor.ram_mb}MB RAM, {flavor.disk_gb}GB disk")
    
    # List images
    print("\n🖥️ Available Images:")
    for image in client.list_images():
        print(f"  {image.name} ({image.id})")
    
    # Create instance
    print("\n🚀 Creating instance...")
    instance = client.create_instance(
        name="web-server-prod",
        image_id="img-ubuntu-2204",
        flavor_id="t1.small",
        key_name="my-keypair"
    )
    print(f"  Created: {instance.name} ({instance.id})")
    print(f"  IP: {instance.ip_address}")
    print(f"  Status: {instance.status.value}")
    
    # Create volume
    print("\n💾 Creating volume...")
    volume = client.create_volume("data-disk", 100, "SSD")
    print(f"  Created: {volume.name} ({volume.id})")
    print(f"  Size: {volume.size_gb}GB")
    print(f"  Status: {volume.status.value}")
    
    # Create network
    print("\n🌐 Creating network...")
    network = client.create_network("prod-network", "10.0.2.0/24", "vxlan")
    print(f"  Created: {network.name} ({network.id})")
    print(f"  CIDR: {network.cidr}")
    
    # List instances
    print("\n📋 All Instances:")
    for inst in client.list_instances():
        print(f"  {inst.name}: {inst.status.value} ({inst.ip_address})")
    
    # Get billing
    print("\n💰 Monthly Billing:")
    billing = client.get_billing_summary()
    print(f"  Compute: ${billing['compute']:.2f}")
    print(f"  Storage: ${billing['storage']:.2f}")
    print(f"  Network: ${billing['network']:.2f}")
    print(f"  Total: ${billing['total']:.2f}")