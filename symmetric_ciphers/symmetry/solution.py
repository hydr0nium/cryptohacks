import requests
import json

def get_flag():
  res = requests.get("https://aes.cryptohack.org/symmetry/encrypt_flag/")
  flag_encrypted_hex = json.loads(res.text)["ciphertext"]
  return flag_encrypted_hex


def encrypt(iv_plaintext_hex: str) -> str:
  iv, plaintext = split_iv(iv_plaintext_hex)
  res = requests.get(f"https://aes.cryptohack.org/symmetry/encrypt/{plaintext}/{iv}/")
  ciphertext_hex = json.loads(res.text)["ciphertext"]
  return ciphertext_hex

def split_iv(iv_text_hex: str) -> str:
  iv = iv_text_hex[:32]
  text = iv_text_hex[32:]
  return iv, text

def xor_byte_strings_hex(left: str, right: str) -> bytes:
  left = bytes.fromhex(left)
  right = bytes.fromhex(right)
  assert len(left)==len(right), f"Not same size {left} ({len(left)}) and {right} ({len(right)})"
  out = b""
  for l,r in zip(left,right):
    out = out + (l ^ r).to_bytes()
  return out


iv, ciphertext_flag = split_iv(get_flag())
size = len(ciphertext_flag)//2
plaintext = ("A" * size).encode().hex()
ciphertext = encrypt(iv + plaintext)
block_cipher_output = xor_byte_strings_hex(plaintext, ciphertext).hex()
flag = xor_byte_strings_hex(ciphertext_flag, block_cipher_output)
print(flag.decode())

#63f098f6044281e682d38010c8825b1e3eb0cc9517f3adc7bf4bfd9f730db8b1a5