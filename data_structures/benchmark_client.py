import socket
import threading
import time
from queue import Queue
from collections import defaultdict

HOST = "127.0.0.1"
PORT = 8080

# =========================
# CONFIG
# =========================
RPS = 15                  # requests per second
DURATION = 10             # seconds test

ENDPOINTS = [
    ("/a", 0.2),   # (path, timeout_seconds)
    ("/b", 0.5),
    ("/c", 1),
]

NUM_WORKERS = 20


# =========================
# Metrics
# =========================
lock = threading.Lock()
stats = defaultdict(lambda: {
    "total": 0,
    "success": 0,
    "timeout": 0,
    "error": 0
})


# =========================
# HTTP request
# =========================
def make_request(path, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((HOST, PORT))

        req = f"GET {path}?timeout_ms={timeout*1000} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        s.sendall(req.encode())

        _ = s.recv(4096)  # đọc response (không cần full)

        return "success"

    except socket.timeout:
        return "timeout"
    except Exception:
        return "error"
    finally:
        s.close()


# =========================
# Worker
# =========================
queue = Queue()

def worker():
    while True:
        path, timeout = queue.get()

        result = make_request(path, timeout)

        with lock:
            stats[path]["total"] += 1
            stats[path][result] += 1

        queue.task_done()


# =========================
# Scheduler (RPS control)
# =========================
def scheduler():
    start = time.time()
    interval = 1.0 / RPS

    i = 0
    while time.time() - start < DURATION:
        path, timeout = ENDPOINTS[i % len(ENDPOINTS)]
        queue.put((path, timeout))

        i += 1
        time.sleep(interval)


# =========================
# Main
# =========================
def main():
    # start workers
    for _ in range(NUM_WORKERS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()

    # run scheduler
    scheduler()

    # wait for all requests done
    queue.join()

    # report
    print("\n=== RESULT ===")
    for path, s in stats.items():
        total = s["total"]
        success = s["success"]
        timeout = s["timeout"]
        error = s["error"]

        success_rate = (success / total * 100) if total else 0

        print(f"\nEndpoint: {path}")
        print(f"  Total   : {total}")
        print(f"  Success : {success}")
        print(f"  Timeout : {timeout}")
        print(f"  Error   : {error}")
        print(f"  Success rate (<= timeout): {success_rate:.2f}%")

if __name__ == "__main__":
    main()