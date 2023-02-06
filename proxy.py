import socket
import threading
import re
from request import Request
from response import Response
from timeparser import Time

class Proxy:
    """
    Initializing the proxy. 
    """
    def __init__(self, host, port, max_queue):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(max_queue)

        self.host = host
        self.port = port
        self.max_queue = max_queue
        self.request_replacements = {}
        self.response_replacements = {}
        self.keep_alive = True
        self.use_cache = False
        self.request_id = 0
        self.cache = {}

    def run(self):
        """
        Run this function to start listening for new connections.
        """
        print("\033[95m" + f"[SERVER STARTED] The server started succesfully ({self.host}, {self.port})" + "\033[0m")
        while True: 
            client_socket, client_address = self.server.accept()
            new_thread = threading.Thread(target=self.handle_request, args=(client_socket, client_address))
            new_thread.start()

    def add_request_replacement(self, match, replacement):
        """
        This function can be used to add strings or regexs that should be replaced in the requests. The data sent to this function is stored in a dictionary called request_replacements.
        """
        self.request_replacements[match] = replacement
            
    def add_response_replacement(self, match, replacement):
        """
        This function can be used to add strings or regexs that should be replaced in the responses. The data sent to this function is stored in a dictionary called request_replacements.
        """
        self.response_replacements[match.encode("utf-8")] = replacement.encode("utf-8")
        
    def manipulate_request(self, request, connection_id):
        """
        This function manipulates a request-object. If the member variable keep_alive is set to false the header Connection will be set to close. Otherwise it will be set to keep-alive. This function also calls the manipulate member-method of Request. We pass request_replacements as a parameter to decide how the request should be manipulated.
        """
        if self.keep_alive:
            request.headers["Connection"] = " keep-alive"
        else:
            request.headers["Connection"] = " close"
            
        request.manipulate(self.request_replacements, connection_id)
        return request

    def manipulate_response(self, response, connection_id):
        """
        This function manipulates a response-object. If the response-object contains text we call the Response member-method manipulate. We pass response_replacements as a parameter to decide how the response should be manipulated.
        """
        if "Content-Type" in response.headers.keys() and "text" in response.headers["Content-Type"]:
            response.manipulate(self.response_replacements, connection_id)
        return response

    def handle_request(self, client_socket, client_address):
        """
        This function is responsible for handling a request.
        """
        self.request_id += 1
        connection_id = self.request_id
        print('\033[94m'+ f"[CONNECTION #{connection_id}] New connection from {client_address}" + '\033[0m')
        try:
            # Receive data from the client
            request = client_socket.recv(4096) 
        except:
            print("\033[91m" + f"[CONNECTION #{connection_id} Error: could not recieve data from {client_address}" + "\033[0m")

        # Create a request instance
        request = Request(request)

        # Check if request was parsed successfully
        if request.valid:
            print("\033[92m" + f"[CONNECTION #{connection_id}] {client_address[0]}: {request.line}" + "\033[0m")
            
            # Only manipulate if request method is "GET"
            if request.method == "GET":

                # Manipulate request
                request = self.manipulate_request(request, connection_id)
                
                # If requested page is in our cache, create response from cache
                response = self.query_cache(request, connection_id) if self.use_cache else False
                
                if not response:
                    response = self.send_request(request, connection_id)
            else:
                response = self.send_request(request, connection_id)

            # Send request to server
            client_socket.sendall(response.encode())
            
            print("\033[92m" + f"[CONNECTION #{connection_id}] The response was sent to the client {client_address}" + "\033[0m")
                
        else:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            print("\033[93m" + f"[CONNECTION #{connection_id}] The request was rejected" + "\033[0m")

        client_socket.close()
       
    def query_cache(self, request, connection_id):
        """
        This function is called from handle_request is the variable use_cache is set to true. Returns a cached response or false.
        """
        if "If-Modified-Since" in request.headers.keys() and request.url in self.cache.keys() and "Last-Modified" in self.cache[request.url].headers.keys():
            if Time(request.headers["If-Modified-Since"]) <= Time(self.cache[request.url].headers["Last-Modified"]):
                print("\033[92m" + f"[CONNECTION #{connection_id}] Requested webpage was retrieved from cache" + "\033[0m")
                return self.cache[request.url]
        return False

    def send_request(self, request, connection_id):
        """
        This function sends the request to the server and returns the response.
        """
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.connect((request.host, 80))
        destination_socket.sendall(request.encode())
        print("\033[92m" + f"[CONNECTION #{connection_id}] The request was sent to the host ({request.host})" + "\033[0m")
        response = self.handle_response(destination_socket, request, connection_id)
        return response

    def handle_response(self, destination_socket, request, connection_id):
        """
        This function handles the response
        """
        response = b""
        try:
            data = destination_socket.recv(4096)
            while data:
                response += data
                data = destination_socket.recv(4096)
            destination_socket.close()
        except:
            print("\033[91m" + f"[CONNECTION #{connection_id}] Failed to receive response from {request.host}" + "\033[0m")
        response = Response(response)
        if response.valid:
            self.cache[request.url] = response 
            response = self.manipulate_response(response, connection_id)
        return response
        
