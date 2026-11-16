
import domain_utils
from dns_cache import DNSCache


class RequestManager:

    def __init__(self, ad_list, sanction_list, config):

        self.ad_list = ad_list
        self.sanction_list = sanction_list
        self.config = config

        self.cache = DNSCache()

    def process_request(self, domain):

        domain = domain.strip().lower().rstrip(".")

        if not domain_utils.validate_domain(domain):
            return {
                "status": "INVALID_INPUT",
                "ip": None,
                "ttl": 0,
                "source": None
            }

        ad_ip = domain_utils.get_ad_list(
            domain,
            self.ad_list,
            self.config
        )

        if ad_ip is not None:
            return {
                "status": "AD_BLOCK",
                "ip": ad_ip,
                "ttl": self.config["local_ttl"],
                "source": "LOCAL"
            }

        sanction_ip = domain_utils.get_sanction_list(
            domain,
            self.sanction_list,
            self.config
        )

        if sanction_ip is not None:
            return {
                "status": "SANCTION",
                "ip": sanction_ip,
                "ttl": self.config["local_ttl"],
                "source": "LOCAL"
            }

        cached_response = self.cache.get(domain)

        if cached_response is not None:

            ip, ttl = cached_response

            return {
                "status": "OK",
                "ip": ip,
                "ttl": ttl,
                "source": "CACHE"
            }

        return {
            "status": "UPSTREAM_REQUIRED",
            "ip": None,
            "ttl": 0,
            "source": "UPSTREAM"
        }

    def save_upstream_response(self, domain, ip, ttl):

        if not domain_utils.validate_domain(domain):
            return

        self.cache.add(domain, ip, ttl)
