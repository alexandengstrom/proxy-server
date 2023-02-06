import unittest
from request import Request
from response import Response
from timeparser import Time
from proxy import Proxy

class TestRequestMethods(unittest.TestCase):

    def test_constructor(self):
        """
        Test that the constructor creates valid request-objects when correct data is given.
        """
        request1 = Request(b"GET http://google.com/hello TEST\r\nHeader: Value\r\n\r\n")
        self.assertEqual(request1.valid, True)
        self.assertEqual(request1.host, "google.com")
        self.assertEqual(request1.url, "http://google.com/hello")
        self.assertEqual(request1.method, "GET")
        self.assertEqual(request1.headers["Header"], " Value")
        self.assertEqual(request1.line, "GET http://google.com/hello TEST")

        request2 = Request(b"POST google.com Test")
        self.assertEqual(request2.host, "google.com")
        self.assertEqual(request2.headers, {})
        self.assertEqual(request2.method, "POST")

        request3 = Request("incorrect data")
        self.assertEqual(request3.valid, False)

        request4 = Request(b"incorrectdata")
        self.assertEqual(request4.valid, False)

        request4 = Request(b"http://www.google.com")
        self.assertEqual(request4.valid, False)

    def test_encode(self):
        """
        Test that the request-object can be encoded to the correct format. If the object is invalid it should return only the original input without changes.
        """
        request1 = Request(b"GET http://google.com/hello TEST\r\nHeader: Value\r\n\r\n")
        self.assertEqual(request1.encode(), b"GET http://google.com/hello TEST\r\nHeader: Value\r\n\r\n")

        request2 = Request("incorrect data")
        self.assertEqual(request2.encode(), "incorrect data")

    def test_manipulate(self):
        """
        Test that it is possible to manipulate the request.
        """
        request1 = Request(b"GET http://google.com/hello TEST\r\nHeader: Value\r\n\r\n")
        manipulations = {"hello": "manipulated"}
        connection_id = 1
        request1.manipulate(manipulations, connection_id)
        self.assertEqual(request1.line, "GET http://google.com/manipulated TEST")

        request2 = Request(b"GET www.host.com/anytext.jpg TEST\r\nHeader: Value\r\n\r\n")
        manipulations = {"(?<=[\s]).*jpg": "http://troll.jpg"}
        connection_id = 1
        request2.manipulate(manipulations, connection_id)
        self.assertEqual(request2.line, "GET http://troll.jpg TEST")

    def test_parse_host(self):
        """
        Test that the host and URL can be parsed.
        """
        request1 = Request(b"GET http://google.com/hello TEST\r\nHeader: Value\r\n\r\n")
        manipulations = {"hello": "manipulated"}
        connection_id = 1
        request1.manipulate(manipulations, connection_id)
        self.assertEqual(request1.url, "http://google.com/hello")
        self.assertEqual(request1.host, "google.com")
        request1.parse_host(request1.line, True)
        self.assertEqual(request1.url,  "http://google.com/manipulated")
        self.assertEqual(request1.host, "google.com")

class TestResponseMethods(unittest.TestCase):
    def test_constructor(self):
        """
        Test that the constructor can create valid response-objects"
        """
        response1 = Response(b"HTTP/1.1 200 OK (text/html)\r\n\r\n")
        self.assertEqual(response1.valid, True)
        self.assertEqual(response1.status_code, "200")
        self.assertEqual(response1.line, "HTTP/1.1 200 OK (text/html)")
        self.assertEqual(response1.headers, {})
        self.assertEqual(response1.body, b"")

        response2 = Response(b"HTTP/1.1 200 OK (text/html)\r\nEncoding: gzip\r\nConnection: close\r\n\r\nThis is the content")
        self.assertEqual(response2.valid, True)
        self.assertEqual(response2.headers["Encoding"], " gzip")
        self.assertEqual(response2.headers["Connection"], " close")
        self.assertEqual(response2.body.decode(), "This is the content")

        response3 = Response(b"bad data")
        self.assertEqual(response3.valid, False)

        

    def test_encode(self):
        """
        Test that the response can be encoded, if the response is invalid the original content is returned.
        """
        response1 = Response(b"HTTP/1.1 200 OK (text/html)\r\nEncoding: gzip\r\nConnection: close\r\n\r\nThis is the content")
        self.assertEqual(response1.encode(), b"HTTP/1.1 200 OK (text/html)\r\nEncoding: gzip\r\nConnection: close\r\n\r\nThis is the content")

        response2 = Response("bad data")
        self.assertEqual(response2.encode(), "bad data")

    def test_manipulate(self):
        """
        Test that it is possible to manipulate a response
        """
        response1 = Response(b"HTTP/1.1 200 OK (text/html)\r\nEncoding: gzip\r\nConnection: close\r\n\r\nThis is smiley")
        manipulations = {b"smiley": b"trolly"}
        connection_id = 1
        response1.manipulate(manipulations, connection_id)
        self.assertEqual(response1.body, b"This is trolly")

        manipulations2 = {b".*trolly": b"new sentence"}
        response1.manipulate(manipulations2, connection_id)
        self.assertEqual(response1.body, b"new sentence")

class TestTimeMethods(unittest.TestCase):
    
    def test_constructor(self):
        """
        Test that the timestamps from requests and responses can be parsed correctly.
        """
        time1 = Time("Fri, 15 Jan 2021 11:35:43 GMT")
        self.assertEqual(time1.year, 2021)
        self.assertEqual(time1.month, 1)
        self.assertEqual(time1.day, 15)
        self.assertEqual(time1.hours, 11)
        self.assertEqual(time1.minutes, 35)
        self.assertEqual(time1.seconds, 43)
        
        time2 = Time("Fri, 1 Jan 1999 00:00:00 GMT")
        self.assertEqual(time2.year, 1999)
        self.assertEqual(time2.month, 1)
        self.assertEqual(time2.day, 1)
        self.assertEqual(time2.hours, 0)
        self.assertEqual(time2.minutes, 0)
        self.assertEqual(time2.seconds, 0)

        time2 = Time("Fri, 31 Dec 2022 23:59:59 GMT")
        self.assertEqual(time2.year, 2022)
        self.assertEqual(time2.month, 12)
        self.assertEqual(time2.day, 31)
        self.assertEqual(time2.hours, 23)
        self.assertEqual(time2.minutes, 59)
        self.assertEqual(time2.seconds, 59)

    def test_operators(self):
        """
        Test that two different times can be compared with operators.
        """
        time1 = Time("Fri, 15 Jan 2021 11:35:43 GMT")
        time2 = Time("Fri, 14 Jan 2021 11:32:43 GMT")
        self.assertTrue(time1 > time2)
        self.assertFalse(time2 > time1)
        self.assertFalse(time1 < time2)
        self.assertTrue(time2 < time1)

        time3 = Time("Fri, 15 Jan 2021 11:31:43 GMT")
        time4 = Time("Fri, 15 Jan 2021 11:31:43 GMT")
        self.assertTrue(time3 >= time4)
        self.assertTrue(time4 >= time3)
        self.assertTrue(time3 <= time4)
        self.assertTrue(time4 <= time3)
        self.assertTrue(time3 == time4)

class TestProxyMethods(unittest.TestCase):

    def test_constructor(self):
        """
        Test that a proxy object can be created correctly
        """
        proxy = Proxy("127.0.0.1", 1234, 10)

        self.assertEqual(proxy.host, "127.0.0.1")
        self.assertEqual(proxy.port, 1234)
        self.assertEqual(proxy.max_queue, 10)
        self.assertEqual(proxy.cache, {})
        self.assertEqual(proxy.keep_alive, True)
        self.assertEqual(proxy.use_cache, False)
        self.assertEqual(proxy.request_replacements, {})
        self.assertEqual(proxy.response_replacements, {})

    def test_add_request_replacement(self):
        """
        Test that we can add strings or regexs that we want to replace in the request.
        """
        proxy = Proxy("127.0.0.1", 1234, 10)
        proxy.add_request_replacement("match", "replacement")
        self.assertEqual(proxy.request_replacements, {"match": "replacement"})

    def test_add_response_replacement(self):
        """
        Test that we can add strings or regexs that we want to replace in the response.
        """
        proxy = Proxy("127.0.0.1", 1234, 10)
        proxy.add_response_replacement("match", "replacement")
        self.assertEqual(proxy.response_replacements, {b"match": b"replacement"})

    def test_manipulate_request(self):
        """
        Test that we can manipulate a request object
        """
        proxy = Proxy("127.0.0.1", 9999, 10)
        proxy.add_request_replacement("(?<= ).*smiley.jpg", "www.newsite.com")
        request1 = Request(b"GET http://google.com/smiley.jpg TEST\r\nHeader: Value\r\n\r\n")
        request1 = proxy.manipulate_request(request1, 1)
        self.assertEqual(request1.line, "GET www.newsite.com TEST")
        self.assertEqual(request1.headers["Connection"], " keep-alive")
        proxy.keep_alive = False
        request1 = proxy.manipulate_request(request1, 1)
        self.assertEqual(request1.headers["Connection"], " close")

    def test_manipulate_response(self):
        """
        Test that we can manipulate a response object.
        """
        proxy = Proxy("127.0.0.1", 9999, 10)
        proxy.add_response_replacement("Smiley", "Trolly")
        response1 = Response(b"HTTP/1.1 200 OK (text/html)\r\nContent-Type: text\r\n\r\nThis is Smiley")
        response1 = proxy.manipulate_response(response1, 1)
        self.assertEqual(response1.body, b"This is Trolly")

    def test_cache(self):
        """
        Test that the proxy can cache responses.
        """
        proxy = Proxy("127.0.0.1", 9999, 10)
        proxy.use_cache = True
        response1 = Response(b"HTTP/1.1 200 OK (text/html)\r\nLast-Modified: Fri, 16 Jan 2021 11:35:43 GMT\r\n\r\nThis is Smiley")
        print(response1.headers)
        proxy.cache["www.smiley.com"] = response1
        request1 =  Request(b"GET www.smiley.com TEST\r\nIf-Modified-Since: Fri, 15 Jan 2021 11:35:43 GMT\r\n\r\n")
        response2 = proxy.query_cache(request1, 1)
        self.assertEqual(response1.body, response2.body)

        request2 =  Request(b"GET www.smiley.com TEST\r\nConnection: close\r\n\r\n")
        response3 = proxy.query_cache(request2, 1)
        self.assertFalse(response3)
        
        
        


if __name__ == "__main__":
    unittest.main()
