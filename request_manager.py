import domain_utils
from dns_cache import DNSCache
from datetime import datetime

class RequestManager:

    def __init__(self, ad_list, sanction_list, config):

        self.ad_list = ad_list
        self.sanction_list = sanction_list
        self.config = config

        self.cache = DNSCache()

    def process_request(self, domain):

        if not isinstance(domain, str):
            return {
                "status": "INVALID_INPUT",
                "ip": None,
                "ttl": None,
                "source": "NONE"
            }

        domain = domain_utils.normalize_domain(domain)

        if not domain_utils.validate_domain(domain):
            return {
                "status": "INVALID_INPUT",
                "ip": None,
                "ttl": None,
                "source": "NONE"
            }

        ad_ip = domain_utils.get_ad_list(
            domain,
            self.ad_list,
            self.config
        )

        if ad_ip is not None:
            return {
                "status": "OK",
                "ip": ad_ip,
                "ttl": self.config["local_ttl"],
                "source": "AD_BLOCK"
            }

        sanction_ip = domain_utils.get_sanction_list(
            domain,
            self.sanction_list,
            self.config
        )

        if sanction_ip is not None:
            return {
                "status": "OK",
                "ip": sanction_ip,
                "ttl": self.config["local_ttl"],
                "source": "SANCTION"
            }

        if self.config["cache_enabled"]:

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
            "ttl": None,
            "source": "UPSTREAM"
        }

    def save_upstream_response(self, domain, ip, ttl):

        if not self.config["cache_enabled"]:
            return

        if not domain_utils.validate_domain(domain):
            return

        if not isinstance(ttl, int) or isinstance(ttl, bool) or ttl <= 0:
            return

        domain = domain_utils.normalize_domain(domain)
        self.cache.add(domain, ip, ttl)

    def log_request(self, domain, result):

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log = (
            f"{current_time} | {domain} | "
            f"{result['source']} | {result['status']} | "
            f"{result['ip'] or '-'} | "
            f"{result['ttl'] if result['ttl'] is not None else '-'}"
        )

        with open("log.txt", "a", encoding="utf-8") as file:
            file.write(log + "\n")
        print(log)
        
    def show_logs(self, filename="log.txt"):
          with open(filename,"r",encoding="utf_8") as file:
              for line in file:
                  print(line.strip())  
                  
    def stats_request(self, filename="log.txt"):
        AD_BLOCK = 0
        SANCTION = 0
        CACHE = 0
        UPSTREAM = 0
        ERRORS = 0 
        TOTAL = 0
        with open(filename,"r", encoding="utf_8") as file:
            for line in file:
                part = line.strip().split("|")
                TOTAL += 1
                if part[2].strip() == "LOCAL" or part[3].strip() == "AD_BLOCK":
                    AD_BLOCK += 1
                elif part[2].strip() == "SANCTION":
                    SANCTION += 1
                elif part[2].strip() == "CACHE":
                    CACHE += 1
                elif part[2].strip() == "UPSTREAM":
                    UPSTREAM += 1
                if part[3].strip() != "AD_BLOCK" and part[3].strip() != "OK":
                    ERRORS += 1
            

        print(f"Total: {TOTAL} | AD_BLOCK: {AD_BLOCK} | SANCTION: {SANCTION} | CACHE: {CACHE} | UPSTREAM: {UPSTREAM} | ERRORS: {ERRORS}")
            
        