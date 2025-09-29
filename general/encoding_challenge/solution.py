from pwn import * # type: ignore # pip install pwntools
import json
import codecs
from Crypto.Util.number import * # type: ignore
from typing import * # type: ignore

r = remote('socket.cryptohack.org', 13377)

def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

while True:
  received = json_recv()
  if "flag" in received:
    print(received["flag"])
    break


  encoding = received["type"]
  encoded = received["encoded"]
  print(f"{encoded} encoded with {encoding}")

  if encoding == "base64":
    decoded = base64.b64decode(encoded).decode("utf-8") # wow so encode
  elif encoding == "hex":
    decoded = bytes.fromhex(encoded).decode("utf-8")
  elif encoding == "rot13":
    decoded = codecs.decode(encoded, 'rot_13')
  elif encoding == "bigint":
    decoded = long_to_bytes(int(encoded, 16)).decode("utf-8")
  elif encoding == "utf-8":
    c = [chr(n) for n in encoded]
    decoded = "".join(c)
  else:
    raise NotImplemented

  to_send = {
    "decoded": decoded
  }

  print(f"Sending {to_send}")
  json_send(to_send)

