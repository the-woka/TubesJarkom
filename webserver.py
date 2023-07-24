from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import mimetypes
import socket

class echoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/pdf':
            self.path = '/TCPSocketProgramming.pdf'
        try:
            file_path = os.path.abspath(self.path[1:])
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                content_type, _ = mimetypes.guess_type(file_path)
                self.send_header('Content-type', content_type)
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            content = b"<html><body><h1>404</h1><h3>File Not Found</h3></body></html>"
            self.send_response(404)
            self.send_header('Content-type', 'text/html')

        self.send_header('Content-length', len(content))
        self.end_headers()
        self.wfile.write(content)

def main():
    HOST = 'localhost'
    PORT = 8000 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f'Server is running on {HOST}:{PORT}')
        while True:
            client_socket, client_address = server_socket.accept()
            handler = echoHandler(client_socket, client_address, server_socket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()