
def get_ad_list(domain, ad_list, config):
    domain = domain.strip().lower().rstrip(".")

    for ad_domain in ad_list:
        ad_domain = ad_domain.strip().lower().rstrip(".")

        if domain == ad_domain or domain.endswith("." + ad_domain):
            return config["sinkhole_ip"]

    return None
   
def get_sanction_list(domain, sanction_list, config):
    domain = domain.strip().lower().rstrip(".")

    for sanction_domain in sanction_list:
        sanction_domain = sanction_domain.strip().lower().rstrip(".")

        if domain == sanction_domain or domain.endswith("." + sanction_domain):
            return config["proxy_ip"]

    return None
def validate_domain(domain):
    domain = domain.strip().lower()

    if domain == "":
        return False

    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-."

    for char in domain:
        if char not in allowed:
            return False

    if domain.startswith("."):
        return False

    if ".." in domain:
        return False

    return True