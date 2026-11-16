import domain_utils

def load_domain_list(filename):
    domains = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if domain_utils.validate_domain(line):
                domain = line.lower().rstrip(".")
                domains.append(domain)

    return domains