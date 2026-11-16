
from request_manager import RequestManager


config = {
    "sinkhole_ip": "0.0.0.0",
    "proxy_ip": "192.0.2.10",
    "local_ttl": 60
}

ad_list = [
    "ads.example.com",
    "both.example.com"
]

sanction_list = [
    "service.example.org",
    "both.example.com"
]


manager = RequestManager(
    ad_list,
    sanction_list,
    config
)


print("TEST 1: Ad Block")
print(manager.process_request("ads.example.com"))


print("\nTEST 2: Sanction")
print(manager.process_request("service.example.org"))


print("\nTEST 3: Ad Block Priority")
print(manager.process_request("both.example.com"))


print("\nTEST 4: Cache Miss")
print(manager.process_request("google.com"))


print("\nTEST 5: Cache Hit")

manager.save_upstream_response(
    "google.com",
    "142.250.185.14",
    60
)

print(manager.process_request("google.com"))


print("\nTEST 6: Invalid Domain")
print(manager.process_request("google com"))
