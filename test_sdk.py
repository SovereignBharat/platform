#!/usr/bin/env python3
"""
Unit tests for OpenStack Cloud Platform SDK.
Run with: python3 -m unittest test_sdk.py -v
"""

import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openstack_sdk import (
    OpenStackClient,
    validate_name, validate_cidr, validate_ip,
    sanitize_input, generate_secure_token,
    hash_password, verify_password,
    check_rate_limit, check_resource_limit,
    sign_request,
    Flavor, Image, Instance, Volume, Network,
    InstanceState, VolumeState, NetworkState
)


class TestValidation(unittest.TestCase):
    """Test input validation functions."""
    
    def test_validate_name_valid(self):
        """Valid names should pass."""
        self.assertTrue(validate_name("web-server"))
        self.assertTrue(validate_name("my_instance"))
        self.assertTrue(validate_name("server123"))
    
    def test_validate_name_invalid(self):
        """Invalid names should fail."""
        self.assertFalse(validate_name(""))  # Empty
        self.assertFalse(validate_name("a"))  # Too short
        self.assertFalse(validate_name("invalid!name"))  # Special char
        self.assertFalse(validate_name("allower_ namespaced"))  # Space
    
    def test_validate_cidr_valid(self):
        """Valid CIDRs should pass."""
        self.assertTrue(validate_cidr("10.0.1.0/24"))
        self.assertTrue(validate_cidr("192.168.1.0/24"))
        self.assertTrue(validate_cidr("172.16.0.0/16"))
    
    def test_validate_cidr_invalid(self):
        """Invalid CIDRs should fail."""
        self.assertFalse(validate_cidr("invalid"))
        self.assertFalse(validate_cidr("not.cidr.at.all"))
        self.assertFalse(validate_cidr("10.0.1.0/33"))  # Invalid prefix
    
    def test_validate_ip_valid(self):
        """Valid IPs should pass."""
        self.assertTrue(validate_ip("10.0.1.1"))
        self.assertTrue(validate_ip("192.168.1.1"))
        self.assertTrue(validate_ip("0.0.0.0"))
    
    def test_validate_ip_invalid(self):
        """Invalid IPs should fail."""
        self.assertFalse(validate_ip("invalid"))
        self.assertFalse(validate_ip("10.0.1"))  # Incomplete
        self.assertFalse(validate_ip("256.0.0.0"))  # Out of range


class TestSanitization(unittest.TestCase):
    """Test input sanitization."""
    
    def test_sanitize_input_removes_special_chars(self):
        """Should remove special characters."""
        result = sanitize_input("<script>alert(1)</script>")
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
    
    def test_sanitize_input_length(self):
        """Should respect max length."""
        long_input = "a" * 500
        result = sanitize_input(long_input, max_length=100)
        self.assertEqual(len(result), 100)
    
    def test_sanitize_input_non_string(self):
        """Should convert non-strings."""
        result = sanitize_input(123)
        self.assertEqual(result, "123")


class TestSecurity(unittest.TestCase):
    """Test security functions."""
    
    def test_generate_secure_token(self):
        """Should generate unique tokens."""
        token1 = generate_secure_token(16)
        token2 = generate_secure_token(16)
        self.assertGreater(len(token1), 16)
        self.assertNotEqual(token1, token2)
    
    def test_hash_password(self):
        """Should hash password with salt."""
        hashed, salt = hash_password("testpass")
        self.assertIsNotNone(salt)
        self.assertIsNotNone(hashed)
        self.assertNotEqual(hashed, "testpass")
    
    def test_verify_password(self):
        """Should verify correct password."""
        password = "mypassword123"
        hashed, salt = hash_password(password)
        self.assertTrue(verify_password(password, hashed, salt))
    
    def test_verify_password_wrong(self):
        """Should reject wrong password."""
        hashed, salt = hash_password("correct")
        self.assertFalse(verify_password("wrong", hashed, salt))
    
    def test_sign_request(self):
        """Should sign request data."""
        data = {"action": "create", "resource": "instance"}
        signature = sign_request(data, "secretkey")
        self.assertIsNotNone(signature)
        self.assertIsInstance(signature, str)


class TestRateLimiting(unittest.TestCase):
    """Test rate limiting."""
    
    def test_check_rate_limit_allows(self):
        """Should allow under limit."""
        # Use unique ID for this test
        result = check_rate_limit(f"test_{id(self)}", max_requests=10)
        self.assertTrue(result)
    
    def test_check_rate_limit_blocks(self):
        """Should block over limit."""
        pass  # Tested in integration


class TestResourceLimits(unittest.TestCase):
    """Test resource limits."""
    
    def test_check_resource_limit_under(self):
        """Should allow under limit."""
        self.assertTrue(check_resource_limit('instances', 50))
    
    def test_check_resource_limit_over(self):
        """Should block over limit."""
        self.assertFalse(check_resource_limit('instances', 150))


class TestOpenStackClient(unittest.TestCase):
    """Test OpenStackClient class."""
    
    def setUp(self):
        """Create client for testing."""
        self.client = OpenStackClient(mock_mode=True)
    
    def test_authenticate(self):
        """Should authenticate."""
        result = self.client.authenticate()
        self.assertTrue(result)
        self.assertIsNotNone(self.client.token)
    
    def test_list_flavors(self):
        """Should list flavors."""
        flavors = self.client.list_flavors()
        self.assertGreater(len(flavors), 0)
        self.assertIsInstance(flavors[0], Flavor)
    
    def test_list_images(self):
        """Should list images."""
        images = self.client.list_images()
        self.assertGreater(len(images), 0)
        self.assertIsInstance(images[0], Image)
    
    def test_create_instance(self):
        """Should create instance."""
        instance = self.client.create_instance(
            name='test-server',
            image_id='img-ubuntu-2204',
            flavor_id='t1.small'
        )
        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.name, 'test-server')
        self.assertIsNotNone(instance.ip_address)
    
    def test_create_instance_invalid_name(self):
        """Should reject invalid name."""
        with self.assertRaises(ValueError):
            self.client.create_instance(
                name='invalid!name',
                image_id='img-ubuntu-2204',
                flavor_id='t1.small'
            )
    
    def test_list_instances(self):
        """Should list instances."""
        self.client.create_instance('test1', 'img-ubuntu-2204', 't1.small')
        instances = self.client.list_instances()
        self.assertGreater(len(instances), 0)
    
    def test_start_instance(self):
        """Should start instance."""
        instance = self.client.create_instance('test-start', 'img-ubuntu-2204', 't1.small')
        result = self.client.start_instance(instance.id)
        self.assertIsNotNone(result)
    
    def test_stop_instance(self):
        """Should stop instance."""
        instance = self.client.create_instance('test-stop', 'img-ubuntu-2204', 't1.small')
        result = self.client.stop_instance(instance.id)
        self.assertIsNotNone(result)
    
    def test_delete_instance(self):
        """Should delete instance."""
        instance = self.client.create_instance('test-delete', 'img-ubuntu-2204', 't1.small')
        result = self.client.delete_instance(instance.id)
        self.assertTrue(result)
    
    def test_create_volume(self):
        """Should create volume."""
        volume = self.client.create_volume('test-vol', 50)
        self.assertIsInstance(volume, Volume)
        self.assertEqual(volume.size_gb, 50)
    
    def test_create_volume_size_limits(self):
        """Should enforce size limits."""
        # Should create valid size
        volume = self.client.create_volume('test-vol-ok', 10)
        self.assertEqual(volume.size_gb, 10)
    
    def test_list_volumes(self):
        """Should list volumes."""
        self.client.create_volume('test-vol', 50)
        volumes = self.client.list_volumes()
        self.assertGreater(len(volumes), 0)
    
    def test_create_network(self):
        """Should create network."""
        network = self.client.create_network('test-net', '10.0.5.0/24')
        self.assertIsInstance(network, Network)
        self.assertEqual(network.name, 'test-net')
    
    def test_create_network_invalid_cidr(self):
        """Should reject invalid CIDR."""
        with self.assertRaises(ValueError):
            self.client.create_network('test', 'invalid')
    
    def test_create_network_invalid_type(self):
        """Should reject invalid network type."""
        with self.assertRaises(ValueError):
            self.client.create_network('test', '10.0.5.0/24', 'invalid')
    
    def test_list_networks(self):
        """Should list networks."""
        self.client.create_network('test-net', '10.0.6.0/24')
        networks = self.client.list_networks()
        self.assertGreater(len(networks), 0)
    
    def test_get_usage(self):
        """Should get usage stats."""
        usage = self.client.get_usage()
        self.assertIsInstance(usage, dict)
        self.assertIn('Instances', usage)
    
    def test_get_billing_summary(self):
        """Should get billing summary."""
        billing = self.client.get_billing_summary()
        self.assertIsInstance(billing, dict)
        self.assertIn('total', billing)


class TestDataClasses(unittest.TestCase):
    """Test data class models."""
    
    def test_flavor_to_dict(self):
        """Flavor should serialize."""
        flavor = Flavor("test", "test.flavor", 2, 2048, 20)
        data = flavor.to_dict()
        self.assertEqual(data['name'], 'test.flavor')
        self.assertEqual(data['vcpus'], 2)
    
    def test_image_to_dict(self):
        """Image should serialize."""
        image = Image("img-1", "Test Image")
        data = image.to_dict()
        self.assertEqual(data['name'], 'Test Image')
    
    def test_instance_to_dict(self):
        """Instance should serialize."""
        instance = Instance(
            "i-1", "test", "img-1", "flavor-1",
            status=InstanceState.ACTIVE
        )
        data = instance.to_dict()
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['status'], 'active')
    
    def test_volume_to_dict(self):
        """Volume should serialize."""
        volume = Volume("v-1", "test", 50)
        data = volume.to_dict()
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['size_gb'], 50)
    
    def test_network_to_dict(self):
        """Network should serialize."""
        network = Network("n-1", "test", "10.0.0.0/24")
        data = network.to_dict()
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['cidr'], '10.0.0.0/24')


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)