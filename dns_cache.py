
import time
import ipaddress


class DNSCache:

    def __init__(self):
        self.cache = []

    def add(self, domain, ip, ttl):

        if ttl <= 0:
            return

        try:
            ipaddress.ip_address(ip)
        except ValueError:
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

        domain = domain.strip().lower().rstrip(".")

        for item in self.cache:

            if item["domain"] == domain:

                elapsed_time = time.monotonic() - item["time"]

                remaining_ttl = item["ttl"] - elapsed_time

                if remaining_ttl <= 0:
                    self.cache.remove(item)
                    return None

                item["ttl"] = remaining_ttl
                item["time"] = time.monotonic()

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
