import domain_utils
from load_domain_list import load_domain_list
test_domains = [
    "google.com",
    "example.net",
    "GOOGLE.COM",
    "google.com.",
    "",
    "google com",
    ".google.com",
    "google..com",
    "google@com"
]

for domain in test_domains:
    result = domain_utils.validate_domain(domain)
    print(domain, "=>", result)
    
ad_list = load_domain_list("ad_list.txt")
sanction_list = load_domain_list("sanction_list.txt")
for i in ad_list:
    print("ad_list:", i)

for j in sanction_list:
    print("sanction_list:", j)
