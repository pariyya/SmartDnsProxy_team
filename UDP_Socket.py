
import socket
import ipaddress
import config


class UDPClient:

    def main(self, domain):

        client_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        try:
            client_socket.settimeout(config.upstream_timeout_sec)

            message = ("QUERY " + domain).encode("utf-8")

            client_socket.sendto(
                message,
                (config.upstream_ip, config.upstream_port)
            )

            receive_data, address_data = client_socket.recvfrom(1024)

            data = receive_data.decode("utf-8").strip()
            parts = data.split()

            if len(parts) == 1 and parts[0] == "NOT_FOUND":
                return "NOT_FOUND", None, None

            if len(parts) == 3 and parts[0] == "OK":

                try:
                    ip = str(ipaddress.IPv4Address(parts[1]))
                    ttl = int(parts[2])
                except (ipaddress.AddressValueError, ValueError):
                    return "SERVER_ERROR", None, None

                if ttl < 0:
                    return "SERVER_ERROR", None, None

                return "OK", ip, ttl

            return "SERVER_ERROR", None, None

        except socket.timeout:
            return "SERVER_ERROR", None, None

        except (ConnectionResetError, OSError, UnicodeDecodeError):
            return "SERVER_ERROR", None, None

        finally:
            client_socket.close()
