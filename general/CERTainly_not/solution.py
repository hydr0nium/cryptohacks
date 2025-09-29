from Crypto.PublicKey import RSA



with open("2048b-rsa-example-cert.der", "b+r") as key_file:
  key = RSA.import_key(key_file.read())
  print(key.n)