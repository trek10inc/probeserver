import os
import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import urllib.request
from socket import gethostbyname 

wait = int(os.getenv('START_WAIT_SECS', '0'))
crash_factor = int(os.getenv('CRASH_FACTOR', '0'))

print(f'waiting {str(wait)}')
time.sleep(wait)

print('Starting application server')

if crash_factor > 0:
    crash_random = random.randint(0,99)
    print(f'crash factor was {str(crash_factor)}, crash random int is {str(crash_random)}')
    if crash_factor > crash_random:
        print('Crashing container')
        quit()
        # raise ValueError('You told me to crash')

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = str(os.getenv('CONTENT', 'EMPTY'))
        my_hostname = str(os.getenv('HOSTNAME', 'localhost'))
        my_ip_address = str(os.getenv('IP_ADDRESS', '127.0.0.1'))
        health_status_factor = int(os.getenv('HEALTH_STATUS_FACTOR', '0'))
        current_request = urllib.parse.urlsplit(self.path)
        # print("path = " + current_request.path)
        try:
            if current_request.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                if content == "EMPTY":
                    content = "Hostname = " + my_hostname + "\n"
                    content += "Ip Address = " + my_ip_address + "\n"
                else:
                    content += "\n"
                self.wfile.write(content.encode("utf-8"))
            elif current_request.path == "/crash":
                print('Crashing container')
                quit()
            elif current_request.path == "/resolve":
                current_request_items = urllib.parse.parse_qs(current_request.query).items()
                current_request = {k: v[0] for k, v in current_request_items}
                if current_request["service"]:
                    url = "http://" + current_request["service"]
                    response = urllib.request.urlopen(url)
                    content = "----------------------------------------------------\n"
                    content += "Hostname = " + my_hostname + "\n"
                    content += "Ip Address = " + my_ip_address + "\n"
                    content += "Service hostname = " + current_request["service"] + "\n"
                    content += "Service IP = " + gethostbyname(current_request["service"]) + "\n"
                    content += "----------------------------------------------------\n"
                    content += response.read().decode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(content.encode("utf-8"))
            elif current_request.path == "/healthz":
                crash_random = random.randint(0,99)
                if health_status_factor > 0 and health_status_factor > crash_random:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    page = '{ "status": "error" }\n' 
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    page = '{ "status": "ok" }\n'
                self.wfile.write(page.encode("utf-8"))
            else:
                self.send_error(404, "File Not Found {}".format(self.path))
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

def main():
    try:
        port = 80
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server is running on port {}".format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print("Stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()
