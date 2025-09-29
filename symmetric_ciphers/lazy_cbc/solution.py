import json
import requests
from Crypto.Cipher import AES
KEY = b"A" * 16


first_block_plain = b"A" * 16
first_block_plain = first_block_plain.hex()
print(f"Sending to encrypt: {first_block_plain}")
res = requests.get(f"https://aes.cryptohack.org/lazy_cbc/encrypt/{first_block_plain}/")
encrypted_block: str = json.loads(res.text)["ciphertext"]
print(f"Received encrpyted: {encrypted_block}")

def xor_byte_strings(left, right):
  assert(len(left)==len(right))
  out = b""
  for l,r in zip(left,right):
    out = out + (l ^ r).to_bytes()
  return out

null_bytes = b"\x00" * 16
ciphertext = null_bytes.hex() + encrypted_block
print(f"Sending ciphertext: {ciphertext}")
res = requests.get(f"https://aes.cryptohack.org/lazy_cbc/receive/{ciphertext}/")
plaintext: str = json.loads(res.text)["error"].split(":")[1]
plaintext = plaintext.strip()
print(f"Received plaintext: {plaintext}")
print(f"Extracting second block")
second_block = plaintext[32:] # Second block is the output of AES when encrypting only A's

print(f"Calculating IV / Key")
key = xor_byte_strings(bytes.fromhex(second_block), b"A" * 16).hex()
print(f"Found key: {key}")
print(f"Extracting flag")
res = requests.get(f"https://aes.cryptohack.org/lazy_cbc/get_flag/{key}/")
flag_hex = json.loads(res.text)["plaintext"]
flag = bytes.fromhex(flag_hex).decode()
print(flag)
111111111111111122222222222222223333333333333333