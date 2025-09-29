from Crypto.Cipher import DES3
import json
import requests

key = "0101010101010101FEFEFEFEFEFEFEFE0101010101010101" # This is a 3DES weak key and makes encryption and decryption the same / flip

res = requests.get(f"https://aes.cryptohack.org/triple_des/encrypt_flag/{key}/") 
flag_encrypted = json.loads(res.text)["ciphertext"]
res = requests.get(f"https://aes.cryptohack.org/triple_des/encrypt/{key}/{flag_encrypted}/") 
flag_hex = json.loads(res.text)["ciphertext"]
flag = bytes.fromhex(flag_hex).split(b"}")[0].decode() + "}"
print(f"Flag: {flag}")
