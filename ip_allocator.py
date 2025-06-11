import ipaddress
from typing import Optional, List, Union


class IPAllocator:
    """
    Allocate IP addresses or subnets from a given network range.
    - supports IPv4 and IPv6.
    - exclusions can be specified to avoid allocating certain IPs or subnets.

    Parameters:
    - network (str): The network range in CIDR notation (e.g., '192.168.1.0/24' or '2001:db8::/32').
    - mask_length (int, optional): The subnet mask length for subnet allocation (e.g., 24 for '/24' subnets).
    - excluded (list of str, optional): A list of network ranges in CIDR notation to exclude from allocation.

    Usage:
    1. IP Allocation:
        allocator = IPAllocator('192.168.1.0/24')
        ip = allocator.allocate()
        print(ip)  # Output: 192.168.1.1

        allocator = IPAllocator('2001:db8::/64')
        ip = allocator.allocate()
        print(ip)  # Output: 2001:db8::1

    2. Subnet Allocation:
        allocator = IPAllocator('192.168.0.0/16', mask_length=24)
        subnet = allocator.allocate()
        print(subnet)  # Output: 192.168.0.0/24

        allocator = IPAllocator('2001:db8::/32', mask_length=48)
        subnet = allocator.allocate()
        print(subnet)  # Output: 2001:db8:0:0::/48

    3. IP Allocation with Exclusions:
        allocator = IPAllocator('192.168.1.0/24', excluded=['192.168.1.1'])
        ip = allocator.allocate()
        print(ip)  # Output: 192.168.1.2

        allocator = IPAllocator('2001:db8::/64', excluded=['2001:db8::1'])
        ip = allocator.allocate()
        print(ip)  # Output: 2001:db8::2

    4. Subnet Allocation with Exclusions:
        allocator = IPAllocator('192.168.0.0/16', mask_length=24, excluded=['192.168.0.0/24'])
        subnet = allocator.allocate()
        print(subnet)  # Output: 192.168.1.0/24

        allocator = IPAllocator('2001:db8::/32', mask_length=48, excluded=['2001:db8:0:0::/48'])
        subnet = allocator.allocate()
        print(subnet)  # Output: 2001:db8:0:1::/48
    """

    def __init__(self, network: str, mask_length: Optional[int] = None, excluded: Optional[List[str]] = None):
        self.network = ipaddress.ip_network(network, strict=False)
        self.mask_length = mask_length
        self.excluded = [ipaddress.ip_network(ex) for ex in excluded] if excluded else []

        self.next_subnet = self.network.subnets(new_prefix=mask_length) if mask_length else None
        self.next_ip = self.network.hosts() if not mask_length else None

    def allocate(self) -> Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address, ipaddress.IPv4Network, ipaddress.IPv6Network]]:
        return self._allocate_subnet() if self.mask_length else self._allocate_ip()

    def _allocate_subnet(self) -> Optional[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]]:
        for subnet in self.next_subnet:
            if not any(subnet.overlaps(ex) for ex in self.excluded):
                return subnet
        return None

    def _allocate_ip(self) -> Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]:
        for ip in self.next_ip:
            if not any(ip in ex for ex in self.excluded):
                return ip
        return None
