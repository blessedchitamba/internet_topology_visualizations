from netaddr import IPNetwork, IPAddress

if IPAddress("192.168.0.1") in IPNetwork("1.0.0.0/24"):
    print("Yay!")