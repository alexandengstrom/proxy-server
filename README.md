# HTTP web proxy
## A content-altering HTTP web proxy developed in python.

### 1. Installation
To run the proxy server the following files are required
- main.py
- proxy.py
- request.py
- response.py
- timeparser.py

You also need Python installed on your machine.

### 2. Configuration
First we create an instance of the proxy, this can be done in the following way:
```
proxy = Proxy("127.0.0.1", 9999, 10)
```
When a new proxy-server is created, three values are required. The first value is the IP-address where the proxy will be hosted. The second value is which port the proxy is going to use. The last value is the maximum numbers of connections in the queue waiting to be accepted.

When an instance of a proxy-server is created, it can be configured to match your requirements:
   
#### Use caching:
``` 
proxy.use_cache = True
```
If use_cache is set to True the proxy will use its own cache to retrieve websites you have already visited without sending a new requests to the server.

#### Close all connections directly:
```
proxy.keep_alive = False
```
If keep_alive is set to False the header "Connection:" will be set to "close" in all requests. Otherwise it is set to "keep-alive".

#### Manipulate requests:
```
proxy.add_request_replacement("match", "replacement")
```
The first parameter "match" should be a regular expression and everything that matches that pattern will be replaced with the parameter "replacement". The proxy will only replace content in the first line of the request when using this method.

#### Manipulate responses:
```
proxy.add_request_replacement("match", "replacement")
```
The first parameter "match" should be a regular expression and everything that matches that pattern will be replaced with the parameter "replacement". The proxy will replace everything in the response-body.

### 3. Run
When the proxy is configured to match your requirements, call the method run to start the server.
```
proxy.run()
```

## Examples
This is how you could configure the proxy server to do the following thing:
- Replace all jpg and png-images to a trollface-picture.

```
from proxy import Proxy

if __name__ == "__main__":
    proxy = Proxy("127.0.0.1", 9999, 10)
    proxy.keep_alive = False
    proxy.use_cache = True
    proxy.add_request_replacement("(?<= ).*.[jpg|png]", "https://yourhost.com/trollface.jpg")
    proxy.run()
```
### How the website would look without the proxy:
![Screenshot from 2023-02-06 14-16-12](https://user-images.githubusercontent.com/123507241/216981401-58acb6c4-29fc-4d4e-ae5b-53bfa43fe092.png)
### How the website would look with the proxy:
![Screenshot from 2023-02-06 14-15-26](https://user-images.githubusercontent.com/123507241/216981564-0417ec72-b613-402a-a437-8a117a5cc572.png)

In this example we want to replace all occurences of the word "Alice" to "Trolly".
```
from proxy import Proxy

if __name__ == "__main__":
    proxy = Proxy("127.0.0.1", 9999, 10)
    proxy.keep_alive = False
    proxy.use_cache = True
    proxy.add_response_replacement('(?<=[\s|"])Alice', 'Trolly')
    proxy.run()
```
### How the website would look without the proxy:
![Screenshot from 2023-02-06 14-21-20](https://user-images.githubusercontent.com/123507241/216985699-46fb91d5-f96f-47f6-819e-8fffe163d552.png)
### How the website would look with the proxy:

![Screenshot from 2023-02-06 14-25-51](https://user-images.githubusercontent.com/123507241/216985768-210ff8a1-1830-4b67-8e15-9fc626a0390f.png)
