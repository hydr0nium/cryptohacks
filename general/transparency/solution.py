import requests
import re


search = requests.get("https://crt.sh/?q=cryptohack.org")
result = re.findall(r">(.*flag.*)<", search.text)
flag = requests.get("http://" + result[0])
print(flag.text)