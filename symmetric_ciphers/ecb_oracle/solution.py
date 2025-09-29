import requests
import json

def encrypt(bytes_in_hex: str) -> str:
  res = requests.get(f"https://aes.cryptohack.org/ecb_oracle/encrypt/{bytes_in_hex}/") # This encrypts my bytes + flag
  ciphertext = json.loads(res.text)["ciphertext"]
  return ciphertext


def create_oracle_block(num_bytes):
  block = b""
  for _ in range(16-num_bytes):
    block += b"A"
  block = block.hex()
  assert(len(block)==(32-num_bytes*2))
  return block

def create_block(string: str):
  block = string.encode().hex()
  assert(len(block)==32)
  return block

def create_guess_block(guess):
  num_bytes = len(guess)
  block = b""
  for _ in range(16-num_bytes):
    block += b"A"
  block += guess
  block = block.hex()
  assert(len(block)==32)
  return block


FOUND_FLAG = b""
FOUND_BYTES_NUM = 0
FOUND_FLAG = ""
OFFSET = 0

charset = "abcdefghijklmnopqrstuvwxyz0123456789_{}&%$.,#+"


# This is really bad code. Please don't hate me
while True:
  for guess in charset:
    padding = FOUND_FLAG
    if len(FOUND_FLAG)>=16:
      padding = FOUND_FLAG[OFFSET:OFFSET+15]
    guess_block = create_guess_block(padding.encode() + guess.encode())
    oracle_block = create_oracle_block(FOUND_BYTES_NUM+1)
    print(f"Using {padding} + {guess} and oracle as {oracle_block} ({len(oracle_block)/2})")
    ciphertext = encrypt(guess_block + oracle_block)
    if ciphertext[:32] in ciphertext[32:]:
      FOUND_FLAG += guess
      print(f"Found character: {FOUND_FLAG}")
      FOUND_BYTES_NUM += 1
      if OFFSET > 0:
        OFFSET +=1
      if guess == "}":
        print(f"Found flag: {FOUND_FLAG}")
        exit()
      break
    if guess == "+":
      print("No guess found")
      exit()
  if len(FOUND_FLAG)%16==0:
    OFFSET += 1
    FOUND_BYTES_NUM = 0




