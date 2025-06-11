import pytest
import ipaddress
from ip_allocator import IPAllocator


def test_ipv4_ip():
    allocator = IPAllocator("192.168.0.0/24")
    ip1 = allocator.allocate()
    assert ip1 == ipaddress.ip_address("192.168.0.1")
    ip2 = allocator.allocate()
    assert ip2 == ipaddress.ip_address("192.168.0.2")


def test_ipv4_ip_exclusions():
    allocator = IPAllocator("192.168.0.0/24", excluded=["192.168.0.1", "192.168.0.2"])
    ip1 = allocator.allocate()
    assert ip1 == ipaddress.ip_address("192.168.0.3")
    ip2 = allocator.allocate()
    assert ip2 == ipaddress.ip_address("192.168.0.4")


def test_ipv4_subnet():
    allocator = IPAllocator("192.168.1.0/24", mask_length=30)
    subnet1 = allocator.allocate()
    assert subnet1 == ipaddress.ip_network("192.168.1.0/30")
    subnet2 = allocator.allocate()
    assert subnet2 == ipaddress.ip_network("192.168.1.4/30")
    subnet3 = allocator.allocate()
    assert subnet3 == ipaddress.ip_network("192.168.1.8/30")


def test_ipv4_subnet_exclusions():
    allocator = IPAllocator(
        "192.168.1.0/24", mask_length=30, excluded=["192.168.1.0/30"]
    )
    subnet1 = allocator.allocate()
    assert subnet1 == ipaddress.ip_network("192.168.1.4/30")
    subnet2 = allocator.allocate()
    assert subnet2 == ipaddress.ip_network("192.168.1.8/30")


def test_ipv4_ip_exhausted():
    allocator = IPAllocator("192.168.0.0/30")  # Only 2 usable IPs
    ip1 = allocator.allocate()
    ip2 = allocator.allocate()
    ip3 = allocator.allocate()
    assert ip3 is None


def test_ipv4_subnet_exhausted():
    allocator = IPAllocator("192.168.0.0/30", mask_length=31)  # Only 2 subnets
    subnet1 = allocator.allocate()
    subnet2 = allocator.allocate()
    subnet3 = allocator.allocate()
    assert subnet3 is None


def test_ipv4_overlapping_exclusions():
    allocator = IPAllocator(
        "192.168.0.0/29", excluded=["192.168.0.0/30", "192.168.0.2/31"]
    )
    ip = allocator.allocate()
    assert ip == ipaddress.ip_address("192.168.0.4")


def test_ipv6_ip():
    allocator = IPAllocator("2001:db8::/32")
    ip1 = allocator.allocate()
    assert ip1 == ipaddress.ip_address("2001:db8::1")
    ip2 = allocator.allocate()
    assert ip2 == ipaddress.ip_address("2001:db8::2")
    ip3 = allocator.allocate()
    assert ip3 == ipaddress.ip_address("2001:db8::3")


def test_ipv6_ip_exclusions():
    allocator = IPAllocator("2001:db8::/32", excluded=["2001:db8::1"])
    ip1 = allocator.allocate()
    assert ip1 == ipaddress.ip_address("2001:db8::2")
    ip2 = allocator.allocate()
    assert ip2 == ipaddress.ip_address("2001:db8::3")
    ip3 = allocator.allocate()
    assert ip3 == ipaddress.ip_address("2001:db8::4")


def test_ipv6_subnet():
    allocator = IPAllocator("2001:db8::/32", mask_length=40)
    subnet1 = allocator.allocate()
    assert subnet1 == ipaddress.ip_network("2001:db8:0000::/40")
    subnet2 = allocator.allocate()
    assert subnet2 == ipaddress.ip_network("2001:db8:0100::/40")
    subnet3 = allocator.allocate()
    assert subnet3 == ipaddress.ip_network("2001:db8:0200::/40")

