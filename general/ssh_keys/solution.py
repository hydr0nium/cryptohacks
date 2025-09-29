from Crypto.PublicKey import RSA



with open("bruce_rsa.pub") as key_file:
  key = RSA.import_key(key_file.read())
  print(key.n)