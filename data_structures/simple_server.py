import socket
import threading
from queue import Queue
from collections import deque
import heapq
from time import sleep, time_ns
from urllib.parse import urlparse, parse_qs

HOST = "0.0.0.0"
PORT = 8080


class ServiceQueue:
    def __init__(self):
        self.q_ = deque()

    def __sizeof__(self):
        return len(self.q_)
    
    def get(self):
        while not self.q_:
            sleep(0.001)
        if self.__sizeof__() <= 10:
            return self.q_.popleft()
        else:
            return self.q_.pop()
    
    def put(self, item):
        return self.q_.append(item)

request_queue = ServiceQueue()

# =========================
# Handlers
# =========================
def handle_a(body):
    sleep(0.1)
    return "A response"

def handle_b(body):
    sleep(0.2)
    return "B response"

def handle_c(body):
    sleep(0.5)
    return "C response"


# =========================
# HTTP parsing
# =========================
def parse_http_request(data: bytes):
    try:
        text = data.decode()
        lines = text.split("\r\n")

        # First line: GET /a?timeout_ms=100 HTTP/1.1
        method, raw_path, _ = lines[0].split()

        parsed = urlparse(raw_path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # convert query: {"timeout_ms": ["100"]} -> {"timeout_ms": "100"}
        query = {k: v[0] for k, v in query.items()}

        # Body
        if "\r\n\r\n" in text:
            body = text.split("\r\n\r\n", 1)[1]
        else:
            body = ""

        return method, path, query, body

    except Exception:
        return None, None, None, None


def build_http_response(body: str, status="200 OK"):
    return (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        f"Content-Type: text/plain\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    ).encode()


# =========================
# Worker thread
# =========================
def worker():
    while True:
        client_socket, method, path, query, body = request_queue.get()
        start_time = time_ns()
        try:
            if path == "/a":
                result = handle_a(body)
            elif path == "/b":
                result = handle_b(body)
            elif path == "/c":
                result = handle_c(body)
            else:
                response = build_http_response("Not Found", "404 Not Found")
                client_socket.sendall(response)
                client_socket.close()
                continue

            response = build_http_response(result)
            client_socket.sendall(response)

        except Exception as e:
            response = build_http_response("Internal Error", "500 Internal Server Error")
            client_socket.sendall(response)

        finally:
            end_time = time_ns()
            client_socket.close()
            print(path, "->", (end_time - start_time) / 1000000, "ms")


# =========================
# Listener thread
# =========================
def listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()

        try:
            data = client_socket.recv(4096)
            method, path, query, body = parse_http_request(data)

            if method is None:
                client_socket.close()
                continue

            request_queue.put((client_socket, method, path, query, body))

        except Exception:
            client_socket.close()


# =========================
# Main
# =========================
if __name__ == "__main__":
    t1 = threading.Thread(target=listener, daemon=True)
    t2 = threading.Thread(target=worker, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()