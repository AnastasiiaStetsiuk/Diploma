from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from supabase import create_client
import os
from calculate_article_risk_scores2 import getImage

SUPABASE_URL = 'https://yndbynxapukqmtykwplw.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InluZGJ5bnhhcHVrcW10eWt3cGx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTQyMTgxNCwiZXhwIjoyMDYwOTk3ODE0fQ.n4ohc1dLfsYtyXb8PvGYrwsfH5JHGFa3DAzJqxSdeyI'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

hostName = "localhost"
serverPort = 8080
#
pageSize = 20

file_path = "a.html" 
file_path2 = "b.html" 
file_path_index = "index.html" 
file_path_diagrams = "c.html" 
def serveFile(self, filePath):
    if os.path.exists(filePath):
        try:
            with open(filePath, 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content)
        except IOError:
            self.send_error(404, 'File Not Found')
    else:
        self.send_error(404, 'File Not Found')

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "" or self.path == "/":
            serveFile(self, file_path_index)
        elif self.path.startswith("/articles"):
            serveFile(self, file_path)
        elif self.path.startswith("/article/"):
            serveFile(self, file_path2)
        elif self.path.startswith("/diagrams"):
            serveFile(self, file_path_diagrams)
        else:
            self.send_error(404, 'File Not Found')
    def do_POST(self):
        if self.path == "/articles":
            postBody = self.rfile.read(int(self.headers.get('Content-length')))
            decoded = postBody.decode('utf-8')
            json_body = json.loads(decoded)
            page = json_body["page"]
            response = supabase.table("articles").select("id", "title").limit(pageSize).offset(pageSize * page).execute()
            json_data = json.dumps(response.data).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header('Content-length', len(json_data))
            self.end_headers()
            
            self.wfile.write(json_data)
        elif self.path == "/article":
            postBody = self.rfile.read(int(self.headers.get('Content-length')))
            decoded = postBody.decode('utf-8')
            json_body = json.loads(decoded)
            id = json_body["article"]
            response = supabase.table("articles").select("*, icrg_risk_components(score, weight, component)").eq("id", id).execute()
            json_data = json.dumps(response.data).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header('Content-length', len(json_data))
            self.end_headers()
            self.wfile.write(json_data)
        elif self.path == "/image":
            postBody = self.rfile.read(int(self.headers.get('Content-length')))
            decoded = postBody.decode('utf-8')
            json_body = json.loads(decoded)
            topic = json_body["topic"]
            arts = supabase.table("articles").select("*, icrg_risk_components(weight), sources(country)").eq("topic", topic).execute().data
            image = getImage(arts)
            self.send_response(200)
            self.send_header("Content-type", "text")
            self.send_header('Content-length', len(image))
            self.end_headers()
            self.wfile.write(image)
        else:
            serveFile(self, file_path)
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")