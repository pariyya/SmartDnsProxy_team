import domain_utils

def load_domain_list(filename):
    domains = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                   continue

                if domain_utils.validate_domain(line):
                   domain = line.lower().rstrip(".")
                   if domain not in domains:
                      domains.append(domain)
                else:
                    print(f"Warning: bad line in {filename}: {line}")
    except OSError:
        raise SystemExit(f"Config error: cannot read {filename}")
    return domains