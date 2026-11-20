
def normalize_domain(domain):

    domain = domain.strip().lower()

    if domain.endswith("."):
        domain = domain[:-1]

    return domain


def validate_domain(domain):

    if not isinstance(domain, str):
        return False

    domain = normalize_domain(domain)

    if not domain:
        return False

    if len(domain) > 253:
        return False

    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-."

    for char in domain:
        if char not in allowed:
            return False

    labels = domain.split(".")

    for label in labels:

        if not label or len(label) > 63:
            return False

        if label.startswith("-") or label.endswith("-"):
            return False

    return True


def get_ad_list(domain, ad_list, config):

    domain = normalize_domain(domain)

    for ad_domain in ad_list:

        ad_domain = normalize_domain(ad_domain)

        if domain == ad_domain or domain.endswith("." + ad_domain):
            return config["sinkhole_ip"]

    return None


def get_sanction_list(domain, sanction_list, config):

    domain = normalize_domain(domain)

    for sanction_domain in sanction_list:

        sanction_domain = normalize_domain(sanction_domain)

        if domain == sanction_domain or domain.endswith("." + sanction_domain):
            return config["proxy_ip"]

    return None
