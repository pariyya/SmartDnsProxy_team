
import config
from request_manager import RequestManager
from UDP_Socket import UDPClient
from load_domain_list import load_domain_list


print("DNS Proxy ready.")

ad_list = load_domain_list(config.ad_list_file)
sanction_list = load_domain_list(config.sanction_list_file)

request_manager = RequestManager(
    ad_list,
    sanction_list,
    config.config
)

client = UDPClient()


while True:

    raw_domain = input("Enter domain (or exit or stats or log or cache): ")

    if raw_domain.strip().lower() == "exit":
        print("Bye.")
        break
    elif raw_domain.strip().lower() == "stats":
        request_manager.stats_request()
        continue
    elif raw_domain.strip().lower() == "log":
        request_manager.show_logs()
        continue
    elif raw_domain.strip().lower() == "cache":
       entries = request_manager.cache.get_all()
       if not entries:
          print("Cache is empty.")
       else:
          for domain, ip, ttl in entries:
              print(f"{domain} | {ip} | {ttl}")
       print(entries)
       continue
    domain = raw_domain.strip().lower().rstrip(".")

    display_domain = domain if domain else "(empty)"

    result = request_manager.process_request(domain)

    if result["status"] == "UPSTREAM_REQUIRED":

        status, ip, ttl = client.main(domain)

        if status == "OK":

            request_manager.save_upstream_response(
                domain,
                ip,
                ttl
            )

            result = {
                "status": "OK",
                "ip": ip,
                "ttl": ttl,
                "source": "UPSTREAM"
            }

        elif status == "NOT_FOUND":

            result = {
                "status": "NOT_FOUND",
                "ip": None,
                "ttl": None,
                "source": "UPSTREAM"
            }

        else:

            result = {
                "status": "SERVER_ERROR",
                "ip": None,
                "ttl": None,
                "source": "UPSTREAM"
            }

    print(f"Domain : {display_domain}")
    print(f"Source : {result['source']}")
    print(f"Status : {result['status']}")
    print(f"IP : {result['ip'] if result['ip'] is not None else '-'}")
    print(f"TTL : {result['ttl'] if result['ttl'] is not None else '-'}")
    print()

    request_manager.log_request(display_domain, result)
