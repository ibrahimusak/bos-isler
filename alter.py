#!/usr/bin/python
from __future__ import print_function
from flask import Flask,render_template,render_template_string
from random_useragent.random_useragent import Randomize
from bs4 import BeautifulSoup
import requests
import random
import os,sys
import string
from flask import request
reload(sys)
sys.setdefaultencoding('utf8')
def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n") or x.endswith("\r"): return x[:-1]
    return x
app = Flask(__name__)	
@app.route("/")
def hello():
    with open('urllist.txt', 'r') as f:
           line=random.sample(f.readlines(),3) 
    return render_template("index.html",line=line)
@app.route('/<variable>/<vari>/')
def sayfaalt(variable,vari):
    git="http://www.pinterest.com/"+variable+"/"+vari+"/"
    adres=request.remote_addr
    try:
        
        return render_template(variable+"-"+vari+".html")
    except:
        if adres!="127.0.0.1":
            return render_template("404.html")
        else:    
            r_agent = Randomize()
            useragent = r_agent.random_agent('desktop','windows')
            with open("proxy.txt") as f:
                lines = f.readlines()
                pr = random.choice(lines)	
            http_proxy  = "http://"+chomp(pr)
            https_proxy = "https://"+chomp(pr)
            proxyDict = { "http"  : http_proxy, "https" : https_proxy}
            headers = {'User-Agent': useragent,
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'}
            r = requests.get(git, headers=headers, proxies=proxyDict)
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup.find_all("meta"):
                if tag.get("property", None) == "og:title":
                    titlecek= tag.get("content", None)
                elif tag.get("property", None) == "og:description":
                    descek= tag.get("content", None)
            with open('sablonalt.txt', 'r') as file :
                filedata = file.read()
            filedata = filedata.replace('<title>Clean Blog </title>', '<title>'+titlecek+'</title>')
            filedata = filedata.replace('<meta name="description" content="desc">', '<meta name="description" content="'+descek+'">')
            filedata = filedata.replace('<a target="_blank" href="adresss">title</a></p>', '<a target="_blank" href="'+git+'">'+titlecek+'</a></p>')
            filedata = filedata.replace('<a target="_blank" href="adress"><i class="next">', '<a target="_blank" href="'+git+'"><i class="next"> ')
            with open(app.root_path+'/templates/'+variable+"-"+vari+'.html', 'w') as file:
                file.write(filedata)
            liste=open("urllist.txt","a")	
            icerik=titlecek+":"+"/"+variable+"/"+vari+"/"
            print(icerik, file=liste)		
            liste.close()
            
        return "ok"+adres
if __name__=="__main__":
    app.run(debug=True)            