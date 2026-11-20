import socket

HOST = "127.0.0.1"
PORT = 5354

request_count = 0


def start_server():

    global request_count

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        server.bind((HOST, PORT))
        print(f"Upstream Server running on {HOST}:{PORT}")

        while True:

            data, address = server.recvfrom(1024)

            request_count += 1

            try:
                message = data.decode("utf-8").strip()
                parts = message.split(maxsplit=1)

                if len(parts) != 2 or parts[0].upper() != "QUERY":
                    domain = "(invalid)"
                    reply = "ERROR"

                else:
                    domain = parts[1].strip().lower().rstrip(".")

                    if not domain:
                        domain = "(invalid)"
                        reply = "ERROR"

                    elif domain == "missing.example.net":
                        reply = "NOT_FOUND"

                    else:
                        reply = "OK 198.51.100.7 5"

            except (UnicodeDecodeError, ValueError):
                domain = "(invalid)"
                reply = "ERROR"

            server.sendto(reply.encode("utf-8"), address)

            print(
                f"Request #{request_count}: {domain} -> {reply}"
            )

    except OSError as error:
        print(f"Upstream Server error: {error}")

    except KeyboardInterrupt:
        print("\nUpstream Server stopped.")

    finally:
        server.close()


if __name__ == "__main__":
    start_server()
