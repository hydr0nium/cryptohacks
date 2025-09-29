import requests
import json
import os
from Crypto.Cipher import AES

class StepUpCounter(object):
    def __init__(self, step_up=False):
        self.value = os.urandom(16).hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))

    def __repr__(self):
        self.increment()
        return self.value

def test():
  ctr = StepUpCounter()
  first = ctr.increment()
  second = ctr.increment()
  assert first == second, "Counter is not constant"
  KEY = b"AAAAAAAAAAAAAAAA"
  cipher = AES.new(KEY, AES.MODE_ECB)
  keystream1 = cipher.encrypt(ctr.increment())
  keystream2 = cipher.encrypt(ctr.increment())
  assert keystream1 == keystream2, "Keystreams are not equal"


def xor_byte_strings_hex(left: str, right: str, check=True) -> bytes:
  left = bytes.fromhex(left)
  right = bytes.fromhex(right)
  if check:
    assert len(left)==len(right), f"Not same size {left} ({len(left)}) and {right} ({len(right)})"
  out = b""
  for l,r in zip(left,right):
    out = out + (l ^ r).to_bytes()
  return out


test()
png_header = "89504E470D0A1A0A0000000D49484452"
res = requests.get("https://aes.cryptohack.org/bean_counter/encrypt/")
image_encrypted = json.loads(res.text)["encrypted"]
first_block = image_encrypted[:32]
key = xor_byte_strings_hex(first_block, png_header).hex()
actual_key = key
while len(actual_key) < len(image_encrypted):
  actual_key += key

image = xor_byte_strings_hex(actual_key, image_encrypted, check=False).hex()

assert len(image) == len(image_encrypted)

with open("bean_flag.png", "b+w") as f:
  f.write(bytes.fromhex(image))
  f.close()
