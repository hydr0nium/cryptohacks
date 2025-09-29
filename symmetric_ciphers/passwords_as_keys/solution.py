


from Crypto.Cipher import AES
import hashlib
import random



def decrypt(ciphertext, key):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return decrypted



ciphertext = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
# /usr/share/dict/words from
# https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words
with open("words.txt") as f:
    words = [w.strip() for w in f.readlines()]
    for word in words:
      #print(f"Trying: {word}")
      KEY = hashlib.md5(word.encode()).digest()
      decrypted = decrypt(ciphertext, KEY)
      if b"crypto" in decrypted:
        print(decrypted)
        exit()
    print("No correct password found")