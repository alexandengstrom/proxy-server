import re

class Request:
    """
    This class represents a HTTP request.
    """
    def __init__(self, content):
        """
        The constructor will take an HTTP request byte string as parameter and parse the data.
        """
        self.content = content
        self.line = ""
        self.method = ""
        self.headers = {}
        self.body = ""
        self.host = ""
        self.url = ""
        self.valid = False
        self.regex = re.compile("[.*\.]*.*/")

        try:
            temp_headers = content.split(b"\r\n\r\n")[0]
            temp_headers = temp_headers.decode("utf-8")
            self.parse_host(temp_headers, True)
            self.method = temp_headers.split()[0]
        
            for index, current_line in enumerate(temp_headers.split("\r\n")):
                if index < 1:
                    self.line = current_line
                elif ":" in current_line:
                    key, value = current_line.split(":", 1)
                    self.headers[key] = value
        except:             
            pass

        
    def encode(self):
        """
        This function will encode all the data in the request back to a byte-string. This function needs to be called before the request is sent to the server.
        """
        if not self.valid:
            return self.content
        request = self.line + "\r\n"
        for key, value in self.headers.items():
            request += ":".join((key, value)) + "\r\n"
        request = (request[0:-2] + "\r\n\r\n").encode("utf-8")
        return request

    def manipulate(self, replacements, connection_id):
        """
        This function manipulates the request, the parameter replacement must be a dictionary where the keys are the values we want to substitute and the values are the new values. It will only replace characters in the line.
        """
        try:
            for match, replacement in replacements.items():
                self.line = re.sub(match, replacement, self.line)
            self.parse_host(self.line, False)
            print("\033[92m" + f"[CONNECTION #{connection_id}] The request was manipulated succesfully" + "\033[0m")
        except:
            print("\033[91m" + f"[CONNECTION #{connection_id}] Failed to manipulate the request" + "\033[0m")

    def parse_host(self, data, update_url):
        """
        This function parses the host. It will also parse the url if update_url i set to true.
        """
        try:
            if self.regex.match(data):
                self.host = data.split("//")[1].split("/")[0]
            else:
                self.host = data.split(" ")[1].split(":")[0]
            if update_url:
                self.url = data.split(" ")[1]
            self.valid = True
        except:
            self.valid = False
