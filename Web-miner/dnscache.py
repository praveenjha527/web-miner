from LRU import LRU
from random import choice
import adns

   
def extract_ipaddrs(resolved_ips):
    ipaddrs = []
    if (len(resolved_ips) > 1):
        for ip in resolved_ips:
            ipaddrs.append(ip[1])
    else:
        ipaddrs.append(resolved_ips[0][1])
    return ipaddrs  

class ResolutionError:
    pass

class DnsCache:
    
    def __init__( self,cache_size):
        self.cache = LRU(cache_size)
 
    def resolve(self,hostname):
        aResolver = adns.init()
        if hostname in self.cache:
            ipaddrs = self.cache.get(hostname)
            if (isinstance(ipaddrs,tuple) and len(ipaddrs) > 1):
                return choice(ipaddrs)
            return ip
        else:
            resolved_ips = (aResolver.synchronous(hostname, adns.rr.ADDR))[3]
            
            if resolved_ips:
                ipaddrs = extract_ipaddrs(resolved_ips)
                self.cache.set(hostname,ipaddrs)
                return ipaddrs
            else:
                raise ResolutionError
    
    def get_ip(self,hostname):
        return choice(self.resolve(hostname))



if __name__ == "__main__":
    TestDnsCache = DnsCache(100)
    print TestDnsCache.get_ip("www.cybersansar.com")
    print TestDnsCache.get_ip("www.cnn.com")
    
              
