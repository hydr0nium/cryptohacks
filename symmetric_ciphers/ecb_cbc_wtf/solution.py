from Crypto.Cipher import AES
import json
import requests


def xor_byte_strings(left, right):
  assert(len(left)==len(right))
  out = b""
  for l,r in zip(left,right):
    out = out + (l ^ r).to_bytes()
  return out


ciphertext_with_iv = "ef8d1de8e5e27d96292c22befcdf2d0673217acd516bd6b057ac9514547c52a581ee079a22477ee68254fab4661b7e5e"
iv = ciphertext_with_iv[:32] # First 16 bytes are IV
ciphertext = ciphertext_with_iv[32:] # Other bytes are ciphertext

assert(len(iv)==32)
assert(len(ciphertext_with_iv)==len(ciphertext)+len(iv))

result = b""

last_block = iv
print(f"Length of ciphertext: {len(ciphertext)}")
for i in range(0, len(ciphertext), 32):
  print(f"Starting block at {i}")
  block = ciphertext[i:i+32] # This should be a block

  d = requests.get("https://aes.cryptohack.org/ecbcbcwtf/decrypt/" + block + "/")
  plaintext = json.loads(d.text)["plaintext"]

  last_block_bytes = bytes.fromhex(last_block)
  plaintext_bytes = bytes.fromhex(plaintext)
  print(f"Decrypting block {(i//32)+1}")
  result += xor_byte_strings(last_block_bytes,plaintext_bytes)
  last_block = block
  
print(result.decode("utf-8"))
