# IPAllocator
Allocate IPv4/v6 addresses or subnets from a given network range.
- supports IPv4 and IPv6.
- exclusions can be specified to avoid allocating certain IPs or subnets.

Parameters:
- network (str): The network range in CIDR notation (e.g., '192.168.1.0/24' or '2001:db8::/32').
- mask_length (int, optional): The subnet mask length for subnet allocation (e.g., 24 for '/24' subnets).
- excluded (list of str, optional): A list of network ranges in CIDR notation to exclude from allocation.

Usage:
1. IP Allocation:
```
    allocator = IPAllocator('192.168.1.0/24')
    ip = allocator.allocate()
    print(ip)  # Output: 192.168.1.1

    allocator = IPAllocator('2001:db8::/64')
    ip = allocator.allocate()
    print(ip)  # Output: 2001:db8::1
```
3. Subnet Allocation:  
```
    allocator = IPAllocator('192.168.0.0/16', mask_length=24)
    subnet = allocator.allocate()
    print(subnet)  # Output: 192.168.0.0/24

    allocator = IPAllocator('2001:db8::/32', mask_length=48)
    subnet = allocator.allocate()
    print(subnet)  # Output: 2001:db8:0:0::/48
```
4. IP Allocation with Exclusions:
```
    allocator = IPAllocator('192.168.1.0/24', excluded=['192.168.1.1'])
    ip = allocator.allocate()
    print(ip)  # Output: 192.168.1.2

    allocator = IPAllocator('2001:db8::/64', excluded=['2001:db8::1'])
    ip = allocator.allocate()
    print(ip)  # Output: 2001:db8::2
```
5. Subnet Allocation with Exclusions:
```
    allocator = IPAllocator('192.168.0.0/16', mask_length=24, excluded=['192.168.0.0/24'])
    subnet = allocator.allocate()
    print(subnet)  # Output: 192.168.1.0/24

    allocator = IPAllocator('2001:db8::/32', mask_length=48, excluded=['2001:db8:0:0::/48'])
    subnet = allocator.allocate()
    print(subnet)  # Output: 2001:db8:0:1::/48
```
