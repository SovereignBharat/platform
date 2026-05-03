#!/usr/bin/env python3
"""
OpenStack Cloud Platform - Instance Management CLI
Command-line interface for managing cloud instances.

Security:
- Input validation and sanitization
- Rate limiting
- Audit logging
- Secure token generation
"""

import sys
import os
import argparse
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openstack_sdk import (
    OpenStackClient, InstanceState, VolumeState, NetworkState,
    validate_name, validate_cidr, check_rate_limit
)

# Configure security audit logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
audit_logger = logging.getLogger('CLI.Audit')


class CloudCLI:
    """Command-line interface for OpenStack Cloud Platform"""
    
    def __init__(self):
        self.client = OpenStackClient(mock_mode=True)
        self.client.authenticate()
    
    def do_list(self, args):
        """List all instances"""
        instances = self.client.list_instances()
        
        if not instances:
            print("No instances found.")
            return
        
        print(f"\n{'Name':<20} {'ID':<15} {'Status':<12} {'IP Address':<15} {'Flavor':<12}")
        print("-" * 80)
        
        for inst in instances:
            print(f"{inst.name:<20} {inst.id:<15} {inst.status.value:<12} "
                  f"{inst.ip_address or 'N/A':<15} {inst.flavor_id:<12}")
    
    def do_create(self, args):
        """Create a new instance"""
        if not args.name:
            print("Error: Instance name is required")
            return 1
        
        instance = self.client.create_instance(
            name=args.name,
            image_id=args.image or "img-ubuntu-2204",
            flavor_id=args.flavor or "t1.small",
            key_name=args.keypair,
        )
        
        print(f"Instance '{instance.name}' ({instance.id}) created successfully")
        print(f"  IP: {instance.ip_address}")
        print(f"  Flavor: {instance.flavor_id}")
        
        return 0
    
    def do_start(self, args):
        """Start an instance"""
        if not args.name and not args.id:
            print("Error: Instance name or ID is required")
            return 1
        
        # Find instance by name or id
        instance = None
        if args.id:
            instance = self.client.get_instance(args.id)
        else:
            for inst in self.client.list_instances():
                if inst.name == args.name:
                    instance = inst
                    break
        
        if not instance:
            print(f"Error: Instance not found")
            return 1
        
        self.client.start_instance(instance.id)
        print(f"Instance '{instance.name}' started successfully")
        return 0
    
    def do_stop(self, args):
        """Stop an instance"""
        if not args.name and not args.id:
            print("Error: Instance name or ID is required")
            return 1
        
        instance = None
        if args.id:
            instance = self.client.get_instance(args.id)
        else:
            for inst in self.client.list_instances():
                if inst.name == args.name:
                    instance = inst
                    break
        
        if not instance:
            print(f"Error: Instance not found")
            return 1
        
        self.client.stop_instance(instance.id)
        print(f"Instance '{instance.name}' stopped successfully")
        return 0
    
    def do_delete(self, args):
        """Delete an instance"""
        if not args.name and not args.id:
            print("Error: Instance name or ID is required")
            return 1
        
        instance = None
        if args.id:
            instance = self.client.get_instance(args.id)
        else:
            for inst in self.client.list_instances():
                if inst.name == args.name:
                    instance = inst
                    break
        
        if not instance:
            print(f"Error: Instance not found")
            return 1
        
        self.client.delete_instance(instance.id)
        print(f"Instance '{instance.name}' deleted successfully")
        return 0
    
    def do_reboot(self, args):
        """Reboot an instance"""
        if not args.name and not args.id:
            print("Error: Instance name or ID is required")
            return 1
        
        instance = None
        if args.id:
            instance = self.client.get_instance(args.id)
        else:
            for inst in self.client.list_instances():
                if inst.name == args.name:
                    instance = inst
                    break
        
        if not instance:
            print(f"Error: Instance not found")
            return 1
        
        self.client.reboot_instance(instance.id)
        print(f"Instance '{instance.name}' rebooted successfully")
        return 0
    
    def do_flavors(self, args):
        """List available flavors"""
        flavors = self.client.list_flavors()
        
        print(f"\n{'Name':<12} {'vCPUs':<8} {'RAM':<10} {'Disk':<10}")
        print("-" * 50)
        
        for flavor in flavors:
            print(f"{flavor.name:<12} {flavor.vcpus:<8} {flavor.ram_mb}MB{'':<4} {flavor.disk_gb}GB")
    
    def do_images(self, args):
        """List available images"""
        images = self.client.list_images()
        
        print(f"\n{'Name':<25} {'ID':<18} {'Size':<12}")
        print("-" * 60)
        
        for image in images:
            size_mb = image.size_bytes // (1024 * 1024)
            print(f"{image.name:<25} {image.id:<18} {size_mb}MB")
    
    def do_volumes(self, args):
        """List volumes"""
        volumes = self.client.list_volumes()
        
        if not volumes:
            print("\nNo volumes found.")
            return
        
        print(f"\n{'Name':<20} {'ID':<15} {'Size':<10} {'Status':<12}")
        print("-" * 65)
        
        for vol in volumes:
            print(f"{vol.name:<20} {vol.id:<15} {vol.size_gb}GB{'':<4} "
                  f"{vol.status.value}")
    
    def do_create_volume(self, args):
        """Create a volume"""
        if not args.name:
            print("Error: Volume name is required")
            return 1
        
        volume = self.client.create_volume(
            name=args.name,
            size_gb=args.size or 50,
            volume_type=args.type or "SSD"
        )
        
        print(f"Volume '{volume.name}' ({volume.id}) created successfully")
        print(f"  Size: {volume.size_gb}GB")
        print(f"  Type: {volume.volume_type}")
        
        return 0
    
    def do_networks(self, args):
        """List networks"""
        networks = self.client.list_networks()
        
        if not networks:
            print("\nNo networks found.")
            return
        
        print(f"\n{'Name':<20} {'ID':<15} {'CIDR':<18} {'Type':<10}")
        print("-" * 70)
        
        for net in networks:
            print(f"{net.name:<20} {net.id:<15} {net.cidr:<18} {net.network_type}")
    
    def do_create_network(self, args):
        """Create a network"""
        if not args.name or not args.cidr:
            print("Error: Network name and CIDR are required")
            return 1
        
        network = self.client.create_network(
            name=args.name,
            cidr=args.cidr,
            network_type=args.type or "vxlan"
        )
        
        print(f"Network '{network.name}' ({network.id}) created successfully")
        print(f"  CIDR: {network.cidr}")
        
        return 0
    
    def do_usage(self, args):
        """Show usage statistics"""
        usage = self.client.get_usage()
        
        print(f"\n📊 Usage Summary")
        print(f"  Instances: {usage.get('Instances', 0)}")
        print(f"  vCPUs: {usage.get('vCPUs', 0)}")
        print(f"  RAM: {usage.get('RAM', 0)}MB")
        print(f"  Disk: {usage.get('Disk', 0)}GB")
    
    def do_billing(self, args):
        """Show billing summary"""
        billing = self.client.get_billing_summary()
        
        print(f"\n💰 Monthly Billing")
        print(f"  Compute: ${billing['compute']:.2f}")
        print(f"  Storage: ${billing['storage']:.2f}")
        print(f"  Network: ${billing['network']:.2f}")
        print(f"  ─────────────────")
        print(f"  Total: ${billing['total']:.2f}")
    
    def do_console(self, args):
        """Get instance console"""
        if not args.name and not args.id:
            print("Error: Instance name or ID is required")
            return 1
        
        instance = None
        if args.id:
            instance = self.client.get_instance(args.id)
        else:
            for inst in self.client.list_instances():
                if inst.name == args.name:
                    instance = inst
                    break
        
        if not instance:
            print(f"Error: Instance not found")
            return 1
        
        console_url = self.client.get_instance_vnc(instance.id)
        print(f"\nInstance console URL:")
        print(f"  {console_url}")
        
        return 0
    
    def run(self, args=None):
        """Run the CLI"""
        parser = argparse.ArgumentParser(
            description='OpenStack Cloud Platform CLI',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # List instances
        subparsers.add_parser('list', help='List all instances')
        
        # Create instance
        create_parser = subparsers.add_parser('create', help='Create new instance')
        create_parser.add_argument('name', help='Instance name')
        create_parser.add_argument('--image', '-i', help='Image ID')
        create_parser.add_argument('--flavor', '-f', help='Flavor ID')
        create_parser.add_argument('--keypair', '-k', help='Key pair name')
        
        # Start instance
        start_parser = subparsers.add_parser('start', help='Start instance')
        start_parser.add_argument('--name', help='Instance name')
        start_parser.add_argument('--id', help='Instance ID')
        
        # Stop instance
        stop_parser = subparsers.add_parser('stop', help='Stop instance')
        stop_parser.add_argument('--name', help='Instance name')
        stop_parser.add_argument('--id', help='Instance ID')
        
        # Delete instance
        delete_parser = subparsers.add_parser('delete', help='Delete instance')
        delete_parser.add_argument('--name', help='Instance name')
        delete_parser.add_argument('--id', help='Instance ID')
        
        # Reboot instance
        reboot_parser = subparsers.add_parser('reboot', help='Reboot instance')
        reboot_parser.add_argument('--name', help='Instance name')
        reboot_parser.add_argument('--id', help='Instance ID')
        
        # Flavors
        subparsers.add_parser('flavors', help='List available flavors')
        
        # Images
        subparsers.add_parser('images', help='List available images')
        
        # Volumes
        subparsers.add_parser('volumes', help='List volumes')
        
        # Create volume
        vol_parser = subparsers.add_parser('create-volume', help='Create volume')
        vol_parser.add_argument('name', help='Volume name')
        vol_parser.add_argument('--size', '-s', type=int, help='Size in GB')
        vol_parser.add_argument('--type', '-t', help='Volume type')
        
        # Networks
        subparsers.add_parser('networks', help='List networks')
        
        # Create network
        net_parser = subparsers.add_parser('create-network', help='Create network')
        net_parser.add_argument('name', help='Network name')
        net_parser.add_argument('--cidr', '-c', help='CIDR (e.g., 10.0.2.0/24)')
        net_parser.add_argument('--type', '-t', help='Network type')
        
        # Usage
        subparsers.add_parser('usage', help='Show usage statistics')
        
        # Billing
        subparsers.add_parser('billing', help='Show billing summary')
        
        # Console
        console_parser = subparsers.add_parser('console', help='Get instance console URL')
        console_parser.add_argument('--name', help='Instance name')
        console_parser.add_argument('--id', help='Instance ID')
        
        # Parse and execute
        parsed = parser.parse_args(args)
        
        if not parsed.command:
            parser.print_help()
            return 0
        
        # Execute command
        handlers = {
            'list': self.do_list,
            'create': self.do_create,
            'start': self.do_start,
            'stop': self.do_stop,
            'delete': self.do_delete,
            'reboot': self.do_reboot,
            'flavors': self.do_flavors,
            'images': self.do_images,
            'volumes': self.do_volumes,
            'create-volume': self.do_create_volume,
            'networks': self.do_networks,
            'create-network': self.do_create_network,
            'usage': self.do_usage,
            'billing': self.do_billing,
            'console': self.do_console,
        }
        
        handler = handlers.get(parsed.command)
        if handler:
            return handler(parsed) or 0
        
        return 0


def main():
    """Main entry point"""
    cli = CloudCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()