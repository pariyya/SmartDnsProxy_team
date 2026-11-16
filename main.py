import domain_utils

print("DNS Proxy ready.")

while True:
    domain = input("enter domain:")

    domain = domain.strip().lower()
    if domain == "":
     print("INVALID_INPUT")
     continue
    if domain == "exit":
        print("Bye")
        break