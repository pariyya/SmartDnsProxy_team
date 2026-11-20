import ipaddress
from pathlib import Path

config = {}

base_dir = Path(__file__).resolve().parent
config_file = base_dir / "config.txt"

try:
    with open(config_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise SystemExit("Config error: invalid config line")

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
    config["upstream_ip"] = str(
        ipaddress.IPv4Address(config["upstream_ip"])
    )
    config["sinkhole_ip"] = str(
        ipaddress.IPv4Address(config["sinkhole_ip"])
    )
    config["proxy_ip"] = str(
        ipaddress.IPv4Address(config["proxy_ip"])
    )
except ipaddress.AddressValueError:
    raise SystemExit("Config error: invalid IP address")


try:
    config["upstream_port"] = int(config["upstream_port"])
except ValueError:
    raise SystemExit("Config error: invalid upstream_port")

if not 1 <= config["upstream_port"] <= 65535:
    raise SystemExit("Config error: invalid upstream_port")


try:
    config["upstream_timeout_sec"] = float(
        config.get("upstream_timeout_sec", "2")
    )
except ValueError:
    raise SystemExit("Config error: invalid upstream_timeout_sec")

if config["upstream_timeout_sec"] <= 0:
    raise SystemExit("Config error: invalid upstream_timeout_sec")


try:
    config["local_ttl"] = int(config.get("local_ttl", "60"))
except ValueError:
    raise SystemExit("Config error: invalid local_ttl")

if config["local_ttl"] <= 0:
    raise SystemExit("Config error: invalid local_ttl")


cache_value = config.get("cache_enabled", "true").lower()


if cache_value == "true":
    config["cache_enabled"] = True
elif cache_value == "false":
    config["cache_enabled"] = False
else:
    raise SystemExit("Config error: invalid cache_enabled")
try:
    config["entries_max_cache"] = int(config.get("entries_max_cache", "2"))
except ValueError:
    raise SystemExit("Config error: invalid entries_max_cache")


config["ad_list_file"] = base_dir / config["ad_list_file"]
config["sanction_list_file"] = base_dir / config["sanction_list_file"]

if not config["ad_list_file"].is_file():
    raise SystemExit("Config error: ad_list_file not found")

if not config["sanction_list_file"].is_file():
    raise SystemExit("Config error: sanction_list_file not found")


upstream_ip = config["upstream_ip"]
upstream_port = config["upstream_port"]
upstream_timeout_sec = config["upstream_timeout_sec"]
sinkhole_ip = config["sinkhole_ip"]
proxy_ip = config["proxy_ip"]
local_ttl = config["local_ttl"]
ad_list_file = config["ad_list_file"]
sanction_list_file = config["sanction_list_file"]
cache_enabled = config["cache_enabled"]
entries_max_cache = config["entries_max_cache"]