
import time
import ipaddress
import math


class DNSCache:

    def __init__(self):
        self.cache = []

    def add(self, domain, ip, ttl):

        if not isinstance(ttl, (int, float)) or ttl <= 0:
           return
            
        try:
            ipaddress.IPv4Address(ip)
        except ValueError:
            return
        if not isinstance(domain, str) or not domain.strip():
            return

        domain = domain.strip().lower().rstrip(".")
    
        self.remove_expired()

        for item in self.cache:
            if item["domain"] == domain:
                item["ip"] = ip
                item["ttl"] = ttl
                item["time"] = time.monotonic()
                return

        self.cache.append({
            "domain": domain,
            "ip": ip,
            "ttl": ttl,
            "time": time.monotonic()
        })

    def get(self, domain):

        if not isinstance(domain, str) or not domain.strip():
           return None
        domain = domain.strip().lower().rstrip(".")
        self.remove_expired()
        for item in self.cache:

            if item["domain"] == domain:

                elapsed_time = time.monotonic() - item["time"]

                remaining_ttl = item["ttl"] - elapsed_time
                remaining_ttl = item["ttl"] - elapsed_time

            if remaining_ttl < 1:
               return None

            return item["ip"], int(remaining_ttl)

        return None

    def remove_expired(self):

        current_time = time.monotonic()

        self.cache = [
            item for item in self.cache
            if item["ttl"] - (current_time - item["time"]) > 0
        ]

    def clear(self):

        self.cache.clear()
