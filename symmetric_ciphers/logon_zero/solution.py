from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long
from os import urandom
#context.log_level = "debug"


def main():
  # test() Disable exploit testing
  s = remote("socket.cryptohack.org", 13399)
  s.recvline()

  # Try login
  while True:
    # Reset password
    packet = b'{"option": "reset_password", "token": "00000000000000000000000000000000000000000000000000000000"}'
    s.sendline(packet)
    print(s.recvline())
    
    packet = b'{"option": "authenticate", "password": ""}'
    s.sendline(packet)
    res = s.recvline()
    print(res)

    if b"flag" in res:
      break

    # Generate new secret key
    packet = b'{"option": "reset_connection"}'
    s.sendline(packet)
    print(s.recvline())


## ----------------- Testing for exploit Area -------------------------


class CFB8:
    def __init__(self, key):
        self.key = key

    def encrypt(self, plaintext):
        IV = urandom(16)
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = b''
        state = IV
        for i in range(len(plaintext)):
            b = cipher.encrypt(state)[0]
            
            c = b ^ plaintext[i]
            ct += bytes([c])
            state = state[1:] + bytes([c])
        return IV + ct

    def decrypt(self, ciphertext):
        IV = ciphertext[:16]
        ct = ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_ECB)
        pt = b''
        state = IV
        for i in range(len(ct)):
            b = cipher.encrypt(state)[0]
            global RUNNING
            global SEEN
            if b not in SEEN:
              SEEN += b.to_bytes()
            print(f"Found {hex(b)} {RUNNING} {SEEN}")
            if b"\x00" in SEEN:
              print("Found zero byte")
            c = b ^ ct[i]
            pt += bytes([c])
            state = state[1:] + bytes([ct[i]])
        return pt

RUNNING = 1
SEEN = b""
def test():
  global RUNNING
  print("Running test")
  while True:
    b = urandom(16)
    cipher = CFB8(b)
    token_ct = bytes.fromhex("00000000000000000000000000000000000000000000000000000000")
    token = cipher.decrypt(token_ct)
    if b"\x00\x00\x00\x00" in token:
      print(f"Token: {token}")
      new_password = token[:-4]
      password_length = bytes_to_long(token[-4:])
      password = new_password[:password_length]
      print(f"Password Length: {password_length}")
      print(f"New Password: {password}")
      exit()
    RUNNING += 1


if __name__ == "__main__":
  main()