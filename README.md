# HTTP web proxy
## A content-altering HTTP web proxy developed in python.

### 1. Installation
To run the proxy server the following files are required

   You also need Python installed on your machine.

2. Configuration
   In the file "main.py" the proxy-server should be configured according to your requirement.

   First we create an instance of the proxy, this can be done in the following way:
   	 proxy = Proxy("127.0.0.1", 9999, 10)

   When a new proxy-server is created, three values are required. The first value is the IP-address where the proxy will be hosted. The second value is which port the proxy is going to use. The last value is the maximum numbers of connections in the queue waiting to be accepted.

   When an instance of a proxy-server is created, it can be configured to match your requirements:
   
   	Use caching:
	proxy.use_cache = True
	If use_cache is set to True the proxy will use its own cache to retrieve websites you have already visited without sending a new requst to the server.

	Close all connections directly:
	proxy.keep_alive = False
	If keep_alive is set to False the header "Connection:" will be set to "close" in all requests. Otherwise it is set to "keep-alive".

	Manipulate requests:
	proxy.add_request_replacement("match", "replacement")
	The first parameter "match" should be a regular expression and everything that matches that pattern will be replaced with the parameter "replacement". The proxy will only replace content in the first line of the request when using this method.

	Manipulate responses:
	proxy.add_request_replacement("match", "replacement")
	The first parameter "match" should be a regular expression and everything that matches that pattern will be replaced with the parameter "replacement". The proxy will replace everything in the response-body.

3. Running the proxy
   Run the proxy by running the command "python3 main.py" in your terminal. You also need to configure your browser to use the the host and port that was chosen in the configuration.
