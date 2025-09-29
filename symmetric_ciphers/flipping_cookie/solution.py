

cookie_plain = "admin=False;expiry="
cookie_ciphertext_and_iv = "5301c24d484595e5cab9ba88dfd9a2e729a22d81eb9bf5989c95d10885552264d3f240702fbc2e9b2cb174a3e98a1a9b"
cookie_iv = cookie_ciphertext_and_iv[:32]
cookie_ciphertext = cookie_ciphertext_and_iv[32:]



first_cookie_block = cookie_plain[:16]
assert(len(first_cookie_block)==16)

def string_to_hex(s: str) -> str:
  return bytes(s).hex()


def xor_byte_strings(left, right) -> bytes:
  assert(len(left)==len(right))
  out = b""
  for l,r in zip(left,right):
    out = out + (l ^ r).to_bytes()
  return out

plaintext_with_iv = xor_byte_strings(first_cookie_block.encode(), bytes.fromhex(cookie_iv))
new_iv = xor_byte_strings(plaintext_with_iv, "admin=True;;expi".encode())
new_iv = new_iv.hex()
new_cookie = new_iv + cookie_ciphertext
print(f"Ciphertext: {cookie_ciphertext}")
print(f"IV: {new_iv}")
print(f"Combined: {new_cookie}")