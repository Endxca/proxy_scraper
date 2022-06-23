#by enderty 2022
import urllib
import requests
import json
from os.path import exists
import re

def test_ip(ip):
  return len(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}",ip))==1

def to_big_lst(text,pl,i):
  tlist=text.split("\n")
  for k in tlist:
    real_ip=k.replace("\n","").replace("\r","")
    if real_ip!="" and test_ip(real_ip):
      if real_ip not in pl[i]:
        pl[i].append(real_ip)
      raw_proxys.write(i+"://"+real_ip+"\n")
  return pl

if exists("proxys.json"):
  proxys=json.load(open("proxys.json","r"))
else:
  proxys={"socks5":[],"socks4":[],"https":[],"http":[]}

print("[*] Getting proxys...")

urls={
      "socks5":
      [["https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",0],
       ["https://www.proxy-list.download/api/v2/get?l=en&t=socks5",2,["LISTA","IP","PORT"]]
       ],
      "socks4":[["https://www.proxy-list.download/api/v2/get?l=en&t=socks4",2,["LISTA","IP","PORT"]]],
      "https":[["https://sslproxies.org/",1,["Updated at","<"]],
               ["https://www.proxy-list.download/api/v2/get?l=en&t=https",2,["LISTA","IP","PORT"]]],
      "http":[["https://www.proxy-list.download/api/v2/get?l=en&t=http",2,["LISTA","IP","PORT"]]]
      }
#thx github
combos=["https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/json/proxies-basic.json"]

raw_proxys=open("raw_proxy.txt","w")


for i in urls:
  for j in urls[i]:
    res=requests.get(j[0])
    if j[1]==0:
      #simply raw data
      raw=res.text.lower()
      proxys=to_big_lst(raw,proxys,i)
    if j[1]==1:
      #complex start and end on page
      start=j[2][0]
      end=j[2][1]
      complicated=res.text.split(start)[1].split(end)[0]
      complicated=complicated.split(" ")[len(complicated.split(" "))-1].lower()
      proxys=to_big_lst(complicated,proxys,i)
    if j[1]==2:
      #json format
      res=json.loads(res.text)[j[2][0]]
      temp_raw=""
      for x in res:
        temp_raw+=x[j[2][1]]+":"+x[j[2][2]]+"\n"
      proxys=to_big_lst(temp_raw,proxys,i)
        
for i in combos:
  res=requests.get(i)
  res=json.loads(res.text)
  temp_raw=""
  for j in res:
    temp_raw+=j["ip"]+":"+str(j["port"])+"\n"
  proxys=to_big_lst(temp_raw,proxys,j["protocols"][0]["type"])


print("[+] All done, *saveing...")
raw_proxys.close()
file=open("proxys.json", "w")
json.dump(proxys,file)
file.close()
print("[+] Goodbye :)")
#  r=requests.get()
