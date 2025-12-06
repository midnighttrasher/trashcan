#QkB$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUOW$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUUUJp&$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUUUUUULh$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUUUUUUUUU0M@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUUUUUUUUUUUCq8$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUUUUUUUUUUUUUUJk$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#UUUUUUUUUUUUUUUUUUUf>.               _____ ____  _____ _____
#UUUUUUUUUUUUUUUUUUUUUYt;.           /    //  __\/  __//  __/
#UUUUUUUUUUUUUUUUUUUUUUUUX?^.        |  __\|  \/||  \  |  \
#UUUUUUUUUUUUUUUUUUUUUUUUUUUx+'      | |   |    /|  /_ |  /_
#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUx+'    \_/   \_/\_\\____\\____\
#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUY)`  ____  ____  _     _____ ____ _____ _  _      _____
#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUx+'   /  __\/  _ \/ \   /  __// ___Y__ __Y \/ \  /|/  __/
#UUUUUUUUUUUUUUUUUUUUUUUUUUUu-'     |  \/|| / \|| |   |  \  |    \ / \ | || |\ |||  \
#UUUUUUUUUUUUUUUUUUUUUUUUY[".       |  __/| |-||| |_/\|  /_ \___ | | | | || | \|||  /_
#UUUUUUUUUUUUUUUUUUUUUUrl.          \_/   \_/ \|\____/\____\\____/ \_/ \_/\_/  \|\____\
#UUUUUUUUUUUUUUUUUUUx+'
#UUUUUUUUUUUUUUUUUJJUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
#UUUUUUUUUUUUUUJJCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#UUUUUUUUUUUUJCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#UUUUUUUUUJCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#UUUUUUJJCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#UUUUJCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
#UJCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC

import socket
import ssl
import importlib
import time
import threading

HOST = None
PORT = None
CHAN = None
USER = None
PW = None
sock = None

# Filled from config.txt
FUNCS = []
NOTIFY = []
JOBS = []
JOINER = []

modules = {}
notifier = {}
handlers = {}
joiner = {}

def fetch():
    global HOST, PORT, CHAN, USER, PW, FUNCS, JOBS, NOTIFY, JOINER
    with open("config.txt", "r") as f:
        line = f.readlines()
        HOST = line[0].strip().split("=")[1]
        PORT = int(line[1].strip().split("=")[1])
        CHAN = line[2].strip().split("=")[1]
        USER = line[3].strip().split("=")[1]
        PW = line[4].strip().split("=")[1]
        FUNCS = [x.strip() for x in line[5].strip().split("=")[1].split(",")]
        JOBS = [x.strip() for x in line[6].strip().split("=")[1].split(";") if x.strip()]
        NOTIFY = [x.strip() for x in line[7].strip().split("=")[1].split(",")]
        JOINER = [x.strip() for x in line[8].strip().split("=")[1].split(",")]


def send_message(target, msg):
    sock.send(f"PRIVMSG {target} :{msg}\r\n".encode())

def registerPlugins(folder, arr, args=None):
    global handlers, JOBS, NOTIFY, modules, notifier, JOINER, joiner
    for name in arr:
        try:
            if args == 'jobs':
                parts = name.split(',')
                jobname = parts[0]
                interval = int(parts[1])
                job = importlib.import_module(f"{folder}.{jobname}")
                modules[jobname] = (job.handle, interval)
                continue
            if args == 'notify':
                notify = importlib.import_module(f"{folder}.{name.split(',')[0]}")
                notifier[name] = notify.handle
                continue
            if args == 'joiner':
                join = importlib.import_module(f"{folder}.{name.split(',')[0]}")
                joiner[name] = join.handle
                continue
            else:
                mod = importlib.import_module(f"{folder}.{name}")
                handlers[name] = mod.handle
                continue

        except Exception as e:
            print(f"[ERR] Failed to load {name}: {e}")


def start_jobs():
    for jobname, jobdata in modules.items():
        func, interval = jobdata
        t = threading.Thread(
            target=func,
            kwargs={
                'bot': __import__(__name__),
                't': interval,
                'channel': CHAN
            }
        )
        t.daemon = True
        t.start()

def process_message(data):
    if " JOIN " in data:
        prefix = data.split("!")[0][1:]
        user = prefix
        channel = data.split(" JOIN ")[1].strip()
        for j in joiner.values():
            j(bot=__import__(__name__), user=user, channel=channel)
        return


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
            time.sleep(0.8)

        if " 900 " in data and not joined:
            time.sleep(0.2)
            sock.send(f"MODE {USER} :-Z\r\n".encode())
            time.sleep(0.4)
            sock.send(f"JOIN {CHAN}\r\n".encode())
            joined = True

        process_message(data)


def init():
    global FUNCS, JOBS, NOTIFY, handlers, modules, notifier
    fetch()
    registerPlugins('funcs', FUNCS)
    registerPlugins('jobs', JOBS, 'jobs')
    registerPlugins('notify', NOTIFY, 'notify')
    registerPlugins('joiner', JOINER, 'joiner')

    start_jobs()
    connect()

if __name__ == "__main__":
    init()
