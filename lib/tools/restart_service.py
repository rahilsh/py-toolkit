# import cgi
#
# import commands
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# from urlparse import parse_qs
#
#
# class GP(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     def do_GET(self):
#         self._set_headers()
#         print(self.path)
#         print(parse_qs(self.path[2:]))
#         self.wfile.write(
#             '<html>    <head>        <title>restart</title>    </head>    <body>        <h1>Enter service name to restart</h1>        <form method="POST" id="serviceForm">            <label>Your service name</label>            <input type="text" name="serviceName" value="" id="serviceName">            <button onsubmit="send()">Submit</button>        </form>    </body></html>')
#
#     def do_POST(self):
#         self._set_headers()
#         form = cgi.FieldStorage(
#             fp=self.rfile,
#             headers=self.headers,
#             environ={'REQUEST_METHOD': 'POST'}
#         )
#         service = form.getvalue("serviceName")
#         status, output = commands.getstatusoutput("sudo service " + service + " restart")
#         if (status == 0):
#             self.wfile.write("<html><body>" + service + " restart success</body></html>")
#         else:q
#             self.wfile.write("<html><body>" + service + " restart failed</body></html>")
#
#
# def run(server_class=HTTPServer, handler_class=GP, port=1234):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#     print('Server running at localhost:1234...')
#     httpd.serve_forever()
#
#
# run()
