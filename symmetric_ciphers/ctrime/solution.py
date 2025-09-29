
import requests
import json

def encrypt(plaintext_hex: str):
  res = requests.get(f"https://aes.cryptohack.org/ctrime/encrypt/{plaintext_hex}/")
  ciphertext = json.loads(res.text)["ciphertext"]
  return ciphertext


def estimate_len_cutoff(estimate_precision=3, base="", charset="abcdefghijklmnopqrstuvwxyz1234567890_{}"):
  sum = 0
  counter = 1
  for guess in charset:
    guess_hex = guess.encode().hex()
    ciphertext = encrypt(to_hex(base) + guess_hex)
    sum += len(ciphertext)
    if counter == 3:
      break
    counter += 1
  return sum//estimate_precision

def to_hex(string: str):
  return string.encode().hex()

charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_{}abcdefghijklmnopqrstuvwxyz!§$%&/()=?[]+-.,@"
FLAG = "crypto{" # Somehow I needed to guess the letter E at some point. IDK why. Maybe new block? See new flag below
FLAG = "crypto{CRIME"
while True:
  average_len = estimate_len_cutoff(base=FLAG, charset=charset)
  for guess in charset:
    guess_hex = guess.encode().hex()
    ciphertext = encrypt(to_hex(FLAG) + guess_hex)
    print(f"Trying: {guess} ({len(ciphertext)}) ({average_len})")
    if len(ciphertext) < average_len:
      print(f"Found guess: {guess} with len {len(ciphertext)} and average of {average_len}")
      FLAG += guess
      print(f"Current found flag: {FLAG}")
      break
      
  if FLAG[-1] == "}":
    break

print(f"Found flag: {FLAG}")