import socket
import time
import config 
class UDPClient:
    def main(self):
     in_from_user = input()
     client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
     try:
         client_socket.settimeout(config.upstream_timeout_sec)
         start_time = time.perf_counter()
         client_socket.sendto(("QUERY " + in_from_user).encode(), (config.upstream_ip, config.upstream_port))
         recieveData, addressData = client_socket.recvfrom(1024)
         end_time = time.perf_counter()
         response_time = end_time - start_time
         data = recieveData.decode()
         parts = data.split()
         if parts[0] != "OK" and parts[0] != "NOT_FOUND":
          print("SERVER ERROR")
         elif parts[0] == "OK" and len(parts) == 3:
             ip = parts[1]
             ttl = int(parts[2])
         elif parts[0] == "NOT_FOUND" and len(parts) == 1:
             print("NOT_FOUND")
         else:
                print("SERVER ERROR")
     except socket.timeout:
         print("SERVER ERROR")
     finally:
         client_socket.close()
