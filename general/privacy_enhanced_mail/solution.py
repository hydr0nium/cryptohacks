from Crypto.PublicKey import RSA



with open("privacy_enhanced_mail.pem") as key_file:
  key = RSA.import_key(key_file.read())
  print(key.d)