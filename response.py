import re

class Response:
    """
    This class represents a HTTP request.
    """
    def __init__(self, content):
        """
        The constructor will take an HTTP response byte string as parameter and parse the data.
        """
        self.content = content
        self.line = ""
        self.status_code = ""
        self.headers = {}
        self.body = ""
        self.valid = False

        try:
            temp_headers, self.body = content.split(b"\r\n\r\n", 1)
            temp_headers = temp_headers.decode()
            self.status_code = temp_headers.split(" ", 2)[1]
            for index, current_line in enumerate(temp_headers.split("\r\n")):
                if index < 1:
                    self.line = current_line
                elif ":" in current_line:
                    key, value = current_line.split(":", 1)
                    self.headers[key] = value
            self.valid = True
            
        except:
            self.valid = False

    def encode(self):
        """
        This function will encode all the data in the response back to a byte-string. This function needs to be called before the response is sent back to the client.
        """
        if not self.valid:
            return self.content
        response = self.line + "\r\n"
        for key, value in self.headers.items():
            response += ":".join((key, value)) + "\r\n"
        response = (response[0:-2] + "\r\n\r\n").encode("utf-8") + self.body
        return response

    def manipulate(self, replacements, connection_id):
        """
        This function manipulates the response, the parameter replacement must be a dictionary where the keys are the values we want to substitute and the values are the new values. It will replace all contents in the body of the response.
        """
        try:
            for match, replacement in replacements.items():
                self.body = re.sub(match, replacement, self.body)
                
            print("\033[92m" + f"[CONNECTION #{connection_id}] The response was manipulated succesfully" + "\033[0m")
        except:
            print("\033[91m" + f"[CONNECTION #{connection_id}] Failed to manipulate the response" + "\033[0m")
