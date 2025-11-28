import socket
import ssl
import importlib

HOST = ""
PORT = 0
CHAN = ""
USER = ""
PW = ""
FUNCS = []

sock = None
handlers = {}

def fetch():
    global HOST, PORT, CHAN, USER, PW, FUNCS
    with open("config.txt", "r") as f:
        line = f.readlines()
        HOST = line[0].strip().split("=")[1]
        PORT = int(line[1].strip().split("=")[1])
        CHAN = line[2].strip().split("=")[1]
        USER = line[3].strip().split("=")[1]
        PW = line[4].strip().split("=")[1]
        FUNCS = [x.strip() for x in line[5].strip().split("=")[1].split(",")]

def send_message(target, msg):
    sock.send(f"PRIVMSG {target} :{msg}\r\n".encode())

def registerFuncs():
    global handlers
    for name in FUNCS:
        try:
            mod = importlib.import_module(f"modules.{name}")
            handlers[name] = mod.handle
            print(f"[OK] Loaded module: {name}")
        except Exception as e:
            print(f"[ERR] Failed to load {name}: {e}")

def process_message(data):
    if "PRIVMSG" not in data or " :" not in data:
        return
    prefix, msg = data.split(" :", 1)
    user = prefix.split("!")[0][1:]
    parts = msg.strip().split(" ")
    if not parts[0].startswith("!"):
        return

    cmd = parts[0][1:]
    args = parts[1:] if len(parts) > 1 else []

    if cmd in handlers:
        handlers[cmd](bot=__import__(__name__), user=user, channel=CHAN, args=args)

def connect():
    global HOST, PORT, CHAN, USER, PW, sock

    context = ssl.create_default_context()
    raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = context.wrap_socket(raw, server_hostname=HOST)
    sock.connect((HOST, PORT))

    sock.send(f"NICK {USER}\r\n".encode())
    sock.send(f"USER {USER} 0 * :{USER}\r\n".encode())

    joined = False
    identified = False

    while True:
        data = sock.recv(4096).decode(errors="ignore")
        print(data, end="")

        if data.startswith("PING"):
            sock.send(data.replace("PING", "PONG").encode())

        if (not identified) and f"NOTICE {USER} :" in data and "This nickname is registered" in data:
            sock.send(f"PRIVMSG NickServ :IDENTIFY {PW}\r\n".encode())
            identified = True

        if (not joined) and (f" 001 {USER} " in data or "You are now identified" in data):
            sock.send(f"JOIN {CHAN}\r\n".encode())
            joined = True

        process_message(data)

def init():
    fetch()
    registerFuncs()
    connect()

if __name__ == "__main__":
    init()
