from Crypto.Util.number import *



# Full python version without pycryptodome
def manual(number: int):
  h = hex(number)
  h = h[2:]
  if len(h) % 2 != 0:
    h = "0" + h
  b = bytes.fromhex(h)
  c = [chr(c) for c in b]
  print("".join(c))
  



def automatic(number: int):
  print(long_to_bytes(number).decode("utf-8"))


n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
automatic(n)
manual(n)

