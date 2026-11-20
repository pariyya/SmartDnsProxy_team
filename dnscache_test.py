from dns_cache import DNSCache
import time
cache = DNSCache()

print("\nTEST 1: Add and Get")
cache.add("google.com", "142.250.185.14", 60)
print(cache.get("google.com"))

print("\nTEST 2: Cache Miss")
print(cache.get("facebook.com"))


print("\nTEST 3: TTL Expiration")
cache.add("test.com", "8.8.8.8", 1)
time.sleep(2)
print(cache.get("test.com"))

print("\nTEST 4: Remove Expired")
cache.add("expired.com", "8.8.4.4", 1)
cache.add("valid.com", "1.1.1.1", 60)
time.sleep(2)
cache.remove_expired()
print(cache.cache) 

print("\nTEST 5: Clear Cache")
cache.clear()
print(cache.cache)

print("\nTEST 6: Update Existing Domain")
cache.add("google.com", "142.250.185.14", 60)
cache.add("google.com", "8.8.8.8", 120)
print(cache.get("google.com"))


print("\nTEST 7: Invalid IP")
cache.add("invalid.com", "999.999.999.999", 60)
print(cache.get("invalid.com"))

print("\nTEST 8: Zero or Negative TTL")
cache.add("zero.com", "8.8.8.8", 0)
cache.add("negative.com", "8.8.8.8", -10)
print(cache.get("zero.com"))
print(cache.get("negative.com"))



