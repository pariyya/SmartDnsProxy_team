
import ipaddress
import math
from pathlib import Path

config = {}
BASE_DIR = Path(__file__).resolve().parent

try:
    with open(BASE_DIR / "config.txt", "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip()

                if key in config:
                   raise SystemExit(f"Config error: duplicate key: {key}")

                config[key.strip()] = value.strip()

            else:
                 raise SystemExit(f"Config error: invalid line: {line}")    

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

    config["upstream_ip"] = upstream_ip
    config["sinkhole_ip"] = sinkhole_ip
    config["proxy_ip"] = proxy_ip
except ipaddress.AddressValueError:
    raise SystemExit("Config error: invalid IP address")

try:
    upstream_port = int(config["upstream_port"])
    config["upstream_port"] = upstream_port
    if not 1 <= upstream_port <= 65535:
        raise SystemExit("Config error: invalid upstream_port")
except ValueError:
    raise SystemExit("Config error: invalid upstream_port")

try:
    upstream_timeout_sec = float(config.get("upstream_timeout_sec", 2))
    config["upstream_timeout_sec"] = upstream_timeout_sec
    if not math.isfinite(upstream_timeout_sec) or upstream_timeout_sec <= 0:
        raise SystemExit("Config error: invalid upstream_timeout_sec")
except ValueError:
    raise SystemExit("Config error: invalid upstream_timeout_sec")

try:
    local_ttl = int(config.get("local_ttl", 60))
    config["local_ttl"]=local_ttl 
    if local_ttl < 0:
        raise SystemExit("Config error: invalid local_ttl")
except ValueError:
    raise SystemExit("Config error: invalid local_ttl")


ad_list_file = BASE_DIR / config["ad_list_file"]
if not ad_list_file.is_file():
    raise SystemExit("Config error: ad_list_file not found")

sanction_list_file = BASE_DIR / config["sanction_list_file"]
if not sanction_list_file.is_file():
    raise SystemExit("Config error: sanction_list_file not found")

config["ad_list_file"] = ad_list_file
config["sanction_list_file"] = sanction_list_file


cache_value = config.get("cache_enabled", "true").lower()

if cache_value == "true":
    cache_enabled = True
elif cache_value == "false":
    cache_enabled = False
else:
    raise SystemExit("Config error: invalid cache_enabled")
config["cache_enabled"] = cache_enabled
