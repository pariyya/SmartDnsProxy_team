
import ipaddress
from pathlib import Path

config = {}

try:
    with open("config.txt", "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

except OSError:
    raise SystemExit("Config error: config.txt not found")

required_keys = [
    "upstream_ip",
    "upstream_port",
    "sinkhole_ip",
    "proxy_ip",
    "ad_list_file",
    "sanction_list_file"
]

for key in required_keys:
    if key not in config or not config[key]:
        raise SystemExit(f"Config error: missing {key}")

try:
    upstream_ip = str(ipaddress.IPv4Address(config["upstream_ip"]))
    sinkhole_ip = str(ipaddress.IPv4Address(config["sinkhole_ip"]))
    proxy_ip = str(ipaddress.IPv4Address(config["proxy_ip"]))
except ipaddress.AddressValueError:
    raise SystemExit("Config error: invalid IP address")

try:
    upstream_port = int(config["upstream_port"])
except ValueError:
    raise SystemExit("Config error: invalid upstream_port")

try:
    upstream_timeout_sec = float(config.get("upstream_timeout_sec", 2))
except ValueError:
    raise SystemExit("Config error: invalid upstream_timeout_sec")

try:
    local_ttl = int(config.get("local_ttl", 60))
except ValueError:
    raise SystemExit("Config error: invalid local_ttl")


ad_list_file = Path(config["ad_list_file"])
if not ad_list_file.is_file():
    raise SystemExit("Config error: ad_list_file not found")

sanction_list_file = Path(config["sanction_list_file"])
if not sanction_list_file.is_file():
    raise SystemExit("Config error: sanction_list_file not found")


cache_value = config.get("cache_enabled", "true").lower()

if cache_value == "true":
    cache_enabled = True
elif cache_value == "false":
    cache_enabled = False
else:
    raise SystemExit("Config error: invalid cache_enabled")
